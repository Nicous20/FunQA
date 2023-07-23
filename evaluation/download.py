from tqdm import tqdm
from otter.modeling_otter import OtterForConditionalGeneration

if __name__ == "__main__":
    model = OtterForConditionalGeneration.from_pretrained(
        "huggingface模型地址", device_map="sequential", cache_dir='自定义本地缓存地址'
    )

model = OtterForConditionalGeneration.from_pretrained(
        "luodian/OTTER-9B-INIT", device_map="sequential", cache_dir='/root/autodl-tmp/hgcache/huggingface/hub'
    )

   