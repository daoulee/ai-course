"""직접 해보기 8. 내 GPU 읽기 (Apple Silicon 버전)

nvidia-smi가 없는 맥에서 같은 정보를 본다.
  python gpu.py        한 번 출력
  python gpu.py -w     1초마다 다시 출력 (Ctrl+C로 종료)
"""

import re
import subprocess
import sys
import time

GB = 1024**3


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


def gpu_name():
    out = sh("system_profiler SPDisplaysDataType")
    chip = re.search(r"Chipset Model: (.+)", out)
    cores = re.search(r"Total Number of Cores: (\d+)", out)
    return f"{chip.group(1) if chip else '?'} ({cores.group(1) if cores else '?'}-core GPU)"


def total_memory():
    return int(sh("sysctl -n hw.memsize"))


def gpu_limit():
    """GPU가 쓸 수 있는 상한. 0이면 기본값(전체의 약 75%)."""
    mb = int(sh("sysctl -n iogpu.wired_limit_mb") or 0)
    return mb * 1024**2 if mb else int(total_memory() * 0.75)


def gpu_stats():
    """ioreg에서 GPU 사용량과 사용률을 꺼낸다. sudo가 필요 없다."""
    out = sh("ioreg -c IOAccelerator -r -d 1 -w 0")
    used = re.search(r'"In use system memory"=(\d+)', out)
    util = re.search(r'"Device Utilization %"=(\d+)', out)
    return int(used.group(1)) if used else 0, int(util.group(1)) if util else 0


def report():
    total, limit = total_memory(), gpu_limit()
    used, util = gpu_stats()
    print(f"GPU            : {gpu_name()}")
    print(f"통합 메모리     : {total / GB:.1f} GB")
    print(f"GPU 사용 상한   : {limit / GB:.1f} GB  (전체의 {limit / total * 100:.0f}%)")
    print(f"GPU 사용 중     : {used / GB:.2f} GB")
    print(f"GPU 사용률      : {util}%")


if __name__ == "__main__":
    if "-w" in sys.argv:
        try:
            while True:
                print("\033[2J\033[H", end="")  # 화면 지우고 커서를 맨 위로
                print(time.strftime("%H:%M:%S"))
                report()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n종료")
    else:
        report()
