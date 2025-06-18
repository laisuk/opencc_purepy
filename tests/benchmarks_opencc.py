import time
from opencc_purepy.core import OpenCC

def benchmark_conversion(input_text: str, config: str = "s2t", rounds: int = 5):
    opencc = OpenCC(config)
    durations = []
    for _ in range(rounds):
        start = time.perf_counter()
        _ = opencc.convert(input_text)
        end = time.perf_counter()
        durations.append((end - start) * 1000)  # Convert to ms
    avg_time = sum(durations) / rounds
    print(f"Input size: {len(input_text):>6} chars | Avg time: {avg_time:.3f} ms over {rounds} runs")


if __name__ == "__main__":
    sample = "潦水尽而寒潭清，烟光凝而暮山紫。俨骖𬴂于上路，访风景于崇阿；临帝子之长洲，得天人之旧馆。层峦耸翠，上出重霄；飞阁流丹，下临无地。"  # or any example text

    for size in [100, 1_000, 10_000, 100_000]:
        # Repeat sample text until desired length
        text = (sample * (size // len(sample) + 1))[:size]
        benchmark_conversion(text)
