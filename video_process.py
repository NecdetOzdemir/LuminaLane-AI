import torch, os, cv2
import numpy as np
import scipy.special
import torchvision.transforms as transforms
from model.model import parsingNet
from PIL import Image
from data.constant import culane_row_anchor, tusimple_row_anchor

class LaneSmoothing:
    """
    Bu sınıf, şeritlerin titremesini engellemek ve süreklilik sağlamak için 
    Zamansal Filtreleme (Temporal Filtering) ve Polinom Uyumu (Polynomial Fitting) kullanır.
    """
    def __init__(self, alpha=0.3, max_history=5):
        self.alpha = alpha # EMA (Üssel Hareketli Ortalama) katsayısı
        self.max_history = max_history # Geçmişte tutulacak kare sayısı
        self.history = {1: {}, 2: {}} # lane_idx -> {row_y -> [list of x values]}

    def smooth(self, lane_idx, points, height):
        # 1. Update history with raw points
        current_rows = {}
        for x, y in points:
            if y not in self.history[lane_idx]:
                self.history[lane_idx][y] = []
            
            # Outlier check: if we have history, ignore points too far from median
            if self.history[lane_idx][y]:
                median_x = np.median(self.history[lane_idx][y])
                if abs(x - median_x) > 50: # Threshold for jumping
                    continue
            
            self.history[lane_idx][y].append(x)
            if len(self.history[lane_idx][y]) > self.max_history:
                self.history[lane_idx][y].pop(0)
            current_rows[y] = x

        # 2. Generate smoothed points for all rows in history
        smoothed_pts = []
        all_y = sorted(self.history[lane_idx].keys())
        for y in all_y:
            if self.history[lane_idx][y]:
                # Weighted average: more weight to current if detected, else use history
                avg_x = np.mean(self.history[lane_idx][y])
                smoothed_pts.append((int(avg_x), int(y)))
        
        # 3. Stabilite ve interpolasyon için polinom uyumu (Curve Fitting) yap
        if len(smoothed_pts) < 5:
            return smoothed_pts # Eğri çizmek için yeterli nokta yoksa ham noktaları dön
        
        pts = np.array(smoothed_pts)
        try:
            # 2. dereceden bir eğri (parabol) uydur: x = ay^2 + by + c
            coeff = np.polyfit(pts[:, 1], pts[:, 0], 2)
            
            # Final pürüzsüz noktaları oluştur (Görselleştirme için 20 nokta yeterli)
            y_range = np.linspace(min(all_y), max(all_y), 20)
            x_fitted = np.polyval(coeff, y_range)
            return [(int(xi), int(yi)) for xi, yi in zip(x_fitted, y_range)]
        except:
            return smoothed_pts

def process_video(video_path, output_path, model_path, dataset='tusimple', callback=None):
    # Load model
    if dataset == 'culane':
        cls_num_per_lane = 18
        row_anchor = culane_row_anchor
        griding_num = 200
    else:
        cls_num_per_lane = 56
        row_anchor = tusimple_row_anchor
        griding_num = 100

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    net = parsingNet(pretrained = False, backbone='18', cls_dim = (griding_num+1, cls_num_per_lane, 4), use_aux=False).to(device)
    state_dict = torch.load(model_path, map_location='cpu')['model']
    compatible_state_dict = {}
    for k, v in state_dict.items():
        if 'module.' in k:
            compatible_state_dict[k[7:]] = v
        else:
            compatible_state_dict[k] = v
    net.load_state_dict(compatible_state_dict, strict=False)
    net.eval()

    img_transforms = transforms.Compose([
        transforms.Resize((288, 800)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    smoother = LaneSmoothing(alpha=0.2)

    print(f"Processing video: {video_path}")
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        if callback and frame_count % 5 == 0:
            progress = int((frame_count / total_frames) * 100)
            callback(progress)

        # Preprocess
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tensor = img_transforms(img_pil).unsqueeze(0).to(device)

        with torch.no_grad():
            out = net(img_tensor)

        # Koordinat dönüşümü: Modelin hücre bazlı çıktısını piksel koordinatına çevir
        col_sample = np.linspace(0, 800 - 1, griding_num)
        col_sample_w = col_sample[1] - col_sample[0]

        out_j = out[0].data.cpu().numpy()
        out_j = out_j[:, ::-1, :]
        # Softmax ile her satırdaki şerit olasılıklarını hesapla (Row Selection)
        prob = scipy.special.softmax(out_j[:-1, :, :], axis=0)
        idx = np.arange(griding_num) + 1
        idx = idx.reshape(-1, 1, 1)
        loc = np.sum(prob * idx, axis=0)
        out_j = np.argmax(out_j, axis=0)
        loc[out_j == griding_num] = 0
        out_j = loc

        # Šerit noktalarını topla ve filtrele (Sadece 1. ve 2. iç şeritler)
        raw_lane_points = {1: [], 2: []}
        for i in [1, 2]:
            if np.sum(out_j[:, i] != 0) > 2:
                for k in range(out_j.shape[0]):
                    if out_j[k, i] > 0:
                        # Row Anchors üzerinden gerçek Y koordinatını hesapla
                        ppp = (int(out_j[k, i] * col_sample_w * width / 800) - 1, int(height * (row_anchor[cls_num_per_lane-1-k]/288)) - 1 )
                        raw_lane_points[i].append(ppp)

        # Yumuşatma ve eğri uydurma algoritmasını uygula
        lane_points = {}
        for i in [1, 2]:
            lane_points[i] = smoother.smooth(i, raw_lane_points[i], height)

        # Draw filled polygon if both inner lanes are detected
        if lane_points[1] and lane_points[2]:
            pts_left = np.array(lane_points[1])
            pts_right = np.array(lane_points[2][::-1]) 
            pts = np.concatenate((pts_left, pts_right), axis=0)
            
            overlay = frame.copy()
            cv2.fillPoly(overlay, [pts], (0, 255, 0))
            cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

        # Draw dots for inner lanes
        for i in [1, 2]:
            if lane_points[i]:
                for ppp in lane_points[i]:
                    cv2.circle(frame, ppp, 5, (0, 255, 0), -1)
        
        out_video.write(frame)
    
    cap.release()
    out_video.release()
    if callback: callback(100)
    print(f"Done! Output saved to {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', type=str, required=True)
    parser.add_argument('--output', type=str, default='output.mp4')
    parser.add_argument('--model', type=str, default='weights/tusimple_18.pth')
    parser.add_argument('--dataset', type=str, default='tusimple')
    args = parser.parse_args()
    
    process_video(args.video, args.output, args.model, args.dataset)
