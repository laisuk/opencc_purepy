import time
import gc
from opencc_purepy.core import OpenCC


def _elapsed_ms(func):
    start = time.perf_counter()
    func()
    return (time.perf_counter() - start) * 1000


def benchmark_conversion(input_text: str, config: str = "s2t", rounds: int = 20):
    cold_total_durations = []
    post_init_cold_durations = []
    warm_durations = []

    for _ in range(rounds):
        gc.collect()

        def cold_total():
            OpenCC(config).convert(input_text)

        cold_total_durations.append(_elapsed_ms(cold_total))

        opencc = OpenCC(config)
        post_init_cold_durations.append(_elapsed_ms(lambda: opencc.convert(input_text)))
        warm_durations.append(_elapsed_ms(lambda: opencc.convert(input_text)))

    cold_total = sum(cold_total_durations) / rounds
    post_init_cold = sum(post_init_cold_durations) / rounds
    warm = sum(warm_durations) / rounds
    print(
        f"Input size: {len(input_text):>6} chars | "
        f"cold_total: {cold_total:.3f} ms | "
        f"post_init_cold: {post_init_cold:.3f} ms | "
        f"warm: {warm:.3f} ms | "
        f"rounds: {rounds}"
    )

if __name__ == "__main__":
    sample = "潦水尽而寒潭清，烟光凝而暮山紫。俨骖𬴂于上路，访风景于崇阿；临帝子之长洲，得天人之旧馆。层峦耸翠，上出重霄；飞阁流丹，下临无地。"  # or any example text

    for size in [100, 1_000, 10_000, 100_000]:
        # Repeat sample text until desired length
        text = (sample * (size // len(sample) + 1))[:size]
        benchmark_conversion(text)
