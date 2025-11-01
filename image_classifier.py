import torch
from torchvision import models, transforms
from PIL import Image
import requests
import io
from typing import Optional, Tuple, Dict

THEME_BUCKETS = {
    "beach": ["sandbar", "seashore", "beach_wagon", "seashore"],
    "food": ["pizza", "hotdog", "cheeseburger", "ice_cream"],
    "vehicle": ["car_wheel", "sports_car", "convertible", "minivan"],
    "people": ["person", "groom", "bride", "maillot"],
    "text_overlay": [],
    "animal": ["dog", "cat", "bird"],
    "urban": ["streetcar", "tower", "building"],
    "unknown": []
}

class ImageThemeClassifier:
    def __init__(self, device: Optional[str] = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = models.mobilenet_v3_large(pretrained=True).to(self.device).eval()
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
         # load imagenet idx->label mapping
        self.idx2label = self._load_imagenet_labels()

    def _load_imagenet_labels(self):
        try:
            from torchvision.models._utils import _get_device
        except Exception:
            pass
        labels = {}
        try:
            with open("assets/imagenet_labels.txt", "r", encoding="utf-8") as fh:
                for i, line in enumerate(fh):
                    labels[i] = line.strip()
        except Exception:
            for i in range(1000):
                labels[i] = f"label_{i}"
        return labels

    def _download_image(self, url: str) -> Optional[Image.Image]:
        if not url:
            return None
        try:
            resp = requests.get(url, timeout=6)
            resp.raise_for_status()
            return Image.open(io.BytesIO(resp.content)).convert("RGB")
        except Exception:
            return None

    def predict_top_label(self, image: Image.Image, topk: int = 3) -> Tuple[str, float]:
        x = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            out = self.model(x)
            probs = torch.nn.functional.softmax(out, dim=1)
            topk_vals, topk_idx = torch.topk(probs, topk)
            idx = topk_idx[0][0].item()
            label = self.idx2label.get(idx, f"label_{idx}")
            score = float(topk_vals[0][0].item())
            return label, score

    def infer_theme(self, media_url: str) -> str:
        img = self._download_image(media_url)
        if img is None:
            return "unknown"
        label, score = self.predict_top_label(img, topk=3)
        for bucket, keywords in THEME_BUCKETS.items():
            for kw in keywords:
                if kw in label.lower():
                    return bucket
        if "person" in label.lower() or "man" in label.lower() or "woman" in label.lower():
            return "people"
        if score < 0.05:
            return "unknown"
        return "unknown"
