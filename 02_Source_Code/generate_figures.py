"""
generate_figures.py
===================
Generates high-resolution academic diagrams for the RSA research report:
1. Figure 1: Operational workflow of the RSA-PSS probabilistic digital signature scheme.
2. Figure 2: Architecture of the proposed off-chain cryptocurrency withdrawal authentication system.
3. Figure 3: Empirical latency distributions for RSA and ECDSA benchmarks (loaded dynamically from CSV).
"""

import csv
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "03_Experimental_Data"
FIG_DIR = PROJECT_ROOT / "04_Figures"

FIG_DIR.mkdir(parents=True, exist_ok=True)


def draw_system_architecture(output_path: Path):
    fig, ax = plt.subplots(figsize=(8.2, 3.1), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 48)

    box_client = dict(boxstyle="round,pad=0.35", fc="#e1f5fe", ec="#0288d1", lw=1.2)
    box_signer = dict(boxstyle="round,pad=0.35", fc="#fff3e0", ec="#f57c00", lw=1.2)
    box_verif = dict(boxstyle="round,pad=0.35", fc="#e8f5e9", ec="#388e3c", lw=1.2)
    box_engine = dict(boxstyle="round,pad=0.35", fc="#ede7f6", ec="#512da8", lw=1.2)
    box_chain = dict(boxstyle="round,pad=0.35", fc="#fce4ec", ec="#c2185b", lw=1.2)

    # Top pipeline
    ax.text(12, 34, "Withdrawal Service\n• Atomic Integer Units\n• Injects UUID Nonce\n• Appends Epoch TS", 
            ha="center", va="center", bbox=box_client, fontsize=7.2)

    ax.text(37, 34, "RSA Signing Component\n• Deterministic JSON\n• SHA-256 Digest\n• RSA-PSS (Env/HSM)", 
            ha="center", va="center", bbox=box_signer, fontsize=7.2)

    ax.text(63, 34, "Verification Gateway\n• Fetch Exchange PubKey\n• Reconstruct Digest\n• RSASSA-PSS-Verify", 
            ha="center", va="center", bbox=box_verif, fontsize=7.2)

    ax.text(88, 34, "Request Validation Engine\n• Nonce Cache (Anti-Replay)\n• Max Skew (±300s)\n• Prototype Check / DB", 
            ha="center", va="center", bbox=box_engine, fontsize=7.2)

    # Bottom chain tier
    ax.text(50, 10, "Blockchain Hot Wallet / Node RPC Gateway\n(Broadcasts Native On-Chain Transactions via secp256k1 ECDSA / BIP 340 Schnorr)", 
            ha="center", va="center", bbox=box_chain, fontsize=7.8, fontweight="bold")

    # Arrows
    ax.annotate("", xy=(25, 34), xytext=(20, 34), arrowprops=dict(arrowstyle="->", lw=1.2, color="#37474f"))
    ax.text(22.5, 36.5, "1. Req", ha="center", fontsize=6.8, fontweight="bold")

    ax.annotate("", xy=(51, 34), xytext=(46, 34), arrowprops=dict(arrowstyle="->", lw=1.2, color="#37474f"))
    ax.text(48.5, 36.5, "2. Signed Req", ha="center", fontsize=6.8, fontweight="bold")

    ax.annotate("", xy=(76, 34), xytext=(71, 34), arrowprops=dict(arrowstyle="->", lw=1.2, color="#37474f"))
    ax.text(73.5, 36.5, "3. Sig Valid", ha="center", fontsize=6.8, fontweight="bold")

    # Approved to Hot Wallet
    ax.annotate("", xy=(65, 14), xytext=(88, 25),
                arrowprops=dict(arrowstyle="->", lw=1.4, color="#2e7d32", connectionstyle="arc3,rad=-0.15"))
    ax.text(84, 18, "4. Approved Request\n(Unique Nonce & Fresh TS)", ha="center", fontsize=7.2, color="#2e7d32", fontweight="bold")

    # Rejection indicators
    ax.text(63, 22, "Invalid Sig → Drop", ha="center", fontsize=6.5, color="#c62828", style="italic")
    ax.text(88, 22, "Replay/Expired → Drop", ha="center", fontsize=6.5, color="#c62828", style="italic")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Architecture diagram saved to: {output_path}")


def draw_rsa_pss_workflow(output_path: Path):
    fig, ax = plt.subplots(figsize=(8.2, 2.7), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 45)

    b_hash = dict(boxstyle="round,pad=0.3", fc="#e0f2f1", ec="#00796b", lw=1.1)
    b_salt = dict(boxstyle="round,pad=0.3", fc="#fff9c4", ec="#fbc02d", lw=1.1)
    b_mgf = dict(boxstyle="round,pad=0.3", fc="#f3e5f5", ec="#7b1fa2", lw=1.1)
    b_math = dict(boxstyle="round,pad=0.3", fc="#ffebee", ec="#d32f2f", lw=1.1)
    b_res = dict(boxstyle="round,pad=0.3", fc="#e8eaf6", ec="#303f9f", lw=1.1)

    ax.text(50, 41, "RSA-PSS Digital Signature Architecture (RFC 8017 / PKCS #1 v2.2)", 
            ha="center", va="center", fontsize=8.5, fontweight="bold")

    ax.text(8, 26, "Message (M)\n[Deterministic JSON]", ha="center", va="center", bbox=b_res, fontsize=7.2)
    ax.text(23, 31, "mHash = H(M)\n(SHA-256)", ha="center", va="center", bbox=b_hash, fontsize=7.2)
    ax.text(23, 19, "Random Salt\n(32 bytes)", ha="center", va="center", bbox=b_salt, fontsize=7.2)

    ax.text(49, 25, "EMSA-PSS Encoding\n• M' = 0x00...00 || mHash || salt\n• H = SHA-256(M')\n• maskedDB = DB ⊕ MGF1(H)\n• EM = maskedDB || H || 0xbc",
            ha="center", va="center", bbox=b_mgf, fontsize=7.0)

    ax.text(78, 25, "RSASP1 Primitive\nS = EM^d mod n\n[Private Key d]", 
            ha="center", va="center", bbox=b_math, fontsize=7.2)

    ax.text(93, 25, "Signature (S)\n256–512 B", ha="center", va="center", bbox=b_res, fontsize=7.2, fontweight="bold")

    ax.annotate("", xy=(16, 28), xytext=(12, 27), arrowprops=dict(arrowstyle="->", lw=1.0))
    ax.annotate("", xy=(34, 28), xytext=(28, 30), arrowprops=dict(arrowstyle="->", lw=1.0))
    ax.annotate("", xy=(34, 22), xytext=(28, 20), arrowprops=dict(arrowstyle="->", lw=1.0))
    ax.annotate("", xy=(69, 25), xytext=(64, 25), arrowprops=dict(arrowstyle="->", lw=1.0))
    ax.annotate("", xy=(87, 25), xytext=(84, 25), arrowprops=dict(arrowstyle="->", lw=1.0))

    ax.text(50, 6, "Verification: Recover EM = S^e mod n using public exponent e; unmask DB with MGF1(H); verify H == SHA-256(M').",
            ha="center", va="center", fontsize=6.8, style="italic", color="#424242")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Workflow diagram saved to: {output_path}")


def draw_benchmark_chart(csv_path: Path, output_path: Path):
    if not csv_path.exists():
        raise FileNotFoundError(f"Benchmark CSV not found: {csv_path}")

    results = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)

    labels = [r["algorithm"] for r in results]
    keygen = [float(r["keygen_median_ms"]) for r in results]
    sign = [float(r["sign_median_ms"]) for r in results]
    verify = [float(r["verify_median_ms"]) for r in results]

    x = np.arange(len(labels))
    width = 0.28

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 2.8), dpi=300)

    # Subplot 1: Keygen (Logarithmic scale)
    bars1 = ax1.bar(x, keygen, width=0.45, color=['#1f77b4', '#1f77b4', '#1f77b4', '#ff7f0e'], edgecolor='black', alpha=0.85)
    ax1.set_title('Key Generation Latency (Median)', fontsize=8.5, fontweight='bold', pad=6)
    ax1.set_xlabel('Cryptographic Algorithm', fontsize=7.5)
    ax1.set_ylabel('Latency (ms, Log Scale)', fontsize=7.5)
    ax1.set_yscale('log')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=7, rotation=10)
    ax1.tick_params(axis='both', labelsize=7)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval * 1.15, f'{yval:.1f}ms', ha='center', va='bottom', fontsize=6.8, fontweight='bold')
    ax1.grid(axis='y', linestyle='--', alpha=0.6)

    # Subplot 2: Signing vs Verification Latency
    rects1 = ax2.bar(x - width/2, sign, width, label='Sign (ms)', color='#d62728', edgecolor='black', alpha=0.85)
    rects2 = ax2.bar(x + width/2, verify, width, label='Verify (ms)', color='#2ca02c', edgecolor='black', alpha=0.85)
    ax2.set_title('Signing vs. Verification Latency (Median)', fontsize=8.5, fontweight='bold', pad=6)
    ax2.set_xlabel('Cryptographic Algorithm', fontsize=7.5)
    ax2.set_ylabel('Latency (ms)', fontsize=7.5)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=7, rotation=10)
    ax2.tick_params(axis='both', labelsize=7)
    ax2.legend(fontsize=7, loc='upper left')
    for bar in rects1:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.15, f'{yval:.2f}', ha='center', va='bottom', fontsize=6.5)
    for bar in rects2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.15, f'{yval:.3f}', ha='center', va='bottom', fontsize=6.5)
    ax2.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Benchmark chart saved to: {output_path}")


def main():
    arch_path = FIG_DIR / "withdrawal_architecture.png"
    wf_path = FIG_DIR / "rsa_pss_workflow.png"
    bench_chart_path = FIG_DIR / "benchmark_performance.png"
    csv_path = DATA_DIR / "benchmark_results.csv"

    draw_system_architecture(arch_path)
    draw_rsa_pss_workflow(wf_path)
    draw_benchmark_chart(csv_path, bench_chart_path)
    print("\nAll figures generated successfully.")


if __name__ == "__main__":
    main()
