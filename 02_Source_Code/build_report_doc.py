"""
build_report_doc.py
===================
Compiles the audited academic research report into Microsoft Word format (.docx):
"Real-World Applications of RSA"

Follows strict consistency and academic rigor:
1. Dynamically reads empirical benchmark results directly from benchmark_results.csv.
2. In-text benchmark statistics, Abstract, and Table 2 are populated from the active dataset.
3. Formulates precise technical distinctions: TLS 1.3 authentication vs key exchange (RFC 9846 / RFC 9963),
   SegWit weight and virtual size (BIP 141), BIP 340 Schnorr vs BIP 327 MuSig2,
   RFC 8017 OAEP size constraints, EMSA-PSS message representatives in Bellcore CRT verification,
   and prototype vs production security boundaries.
4. Uses project-relative paths via pathlib.
5. Strictly targets between 4 and 5 A4 pages (absolute maximum 5 pages).
"""

import os
import csv
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# Project-relative path resolution
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "03_Experimental_Data"
FIG_DIR = PROJECT_ROOT / "04_Figures"
REPORT_DIR = PROJECT_ROOT / "01_Final_Report"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_benchmark_data(csv_path: Path):
    if not csv_path.exists():
        raise FileNotFoundError(f"Benchmark CSV not found at: {csv_path}")
    data = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row["algorithm"]] = row
    return data


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=25, bottom=25, left=40, right=40):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)


def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="8" w:space="0" w:color="1A237E"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="1A237E"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def add_header_footer(section):
    footer = section.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    f_run = f_p.add_run("Page ")
    f_run.font.name = "Times New Roman"
    f_run.font.size = Pt(8.5)
    f_run.font.color.rgb = RGBColor(120, 120, 120)

    fldSimple_page = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    f_p._p.append(fldSimple_page)

    f_run2 = f_p.add_run(" of ")
    f_run2.font.name = "Times New Roman"
    f_run2.font.size = Pt(8.5)
    f_run2.font.color.rgb = RGBColor(120, 120, 120)

    fldSimple_numpages = parse_xml(r'<w:fldSimple %s w:instr="NUMPAGES"/>' % nsdecls('w'))
    f_p._p.append(fldSimple_numpages)

    header = section.header
    h_p = header.paragraphs[0]
    h_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    h_run = h_p.add_run("Academic Research Report | Real-World Applications of RSA")
    h_run.font.name = "Times New Roman"
    h_run.font.size = Pt(8.5)
    h_run.font.italic = True
    h_run.font.color.rgb = RGBColor(128, 128, 128)


def generate_report():
    bench_csv = DATA_DIR / "benchmark_results.csv"
    bench = load_benchmark_data(bench_csv)

    # Dynamic metrics
    r2048 = bench["RSA-2048"]
    r3072 = bench["RSA-3072"]
    r4096 = bench["RSA-4096"]
    ecdsa = bench["ECDSA-secp256k1"]

    r2048_ver_ms = float(r2048["verify_median_ms"])
    r3072_ver_ms = float(r3072["verify_median_ms"])
    r4096_ver_ms = float(r4096["verify_median_ms"])
    ecdsa_ver_ms = float(ecdsa["verify_median_ms"])
    ecdsa_sign_ms = float(ecdsa["sign_median_ms"])
    r3072_sign_ms = float(r3072["sign_median_ms"])
    ecdsa_kg_ms = float(ecdsa["keygen_median_ms"])
    r3072_kg_ms = float(r3072["keygen_median_ms"])

    ratio_2048_ec = round(ecdsa_ver_ms / r2048_ver_ms, 2) if r2048_ver_ms > 0 else 0
    ratio_3072_ec = round(ecdsa_ver_ms / r3072_ver_ms, 2) if r3072_ver_ms > 0 else 0
    ratio_4096_ec = round(ecdsa_ver_ms / r4096_ver_ms, 2) if r4096_ver_ms > 0 else 0
    ratio_sign_ec = round(r3072_sign_ms / ecdsa_sign_ms, 2) if ecdsa_sign_ms > 0 else 0
    ratio_kg_ec = round(r3072_kg_ms / ecdsa_kg_ms, 1) if ecdsa_kg_ms > 0 else 0

    doc = docx.Document()

    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.45)
    section.bottom_margin = Cm(1.45)
    section.left_margin = Cm(1.60)
    section.right_margin = Cm(1.60)

    add_header_footer(section)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(9.5)
    normal_style.font.color.rgb = RGBColor(33, 33, 33)

    def add_p(text="", space_before=0, space_after=0.4, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = doc.add_paragraph(text)
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        return p

    def add_h1(text):
        p = add_p(space_before=1.5, space_after=0.2, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.LEFT)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.0)
        run.font.color.rgb = RGBColor(26, 35, 126)
        return p

    def add_h2(text):
        p = add_p(space_before=1.5, space_after=0.3, line_spacing=1.01, align=WD_ALIGN_PARAGRAPH.LEFT)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10.0)
        run.font.color.rgb = RGBColor(40, 53, 147)
        return p

    # -------------------------------------------------------------
    # TITLE & METADATA
    # -------------------------------------------------------------
    p_title = add_p(space_before=0, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_t = p_title.add_run("Real-World Applications of RSA:\nCryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication")
    r_t.bold = True
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(13.5)
    r_t.font.color.rgb = RGBColor(13, 71, 161)

    p_meta = add_p(space_before=1, space_after=3.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_m = p_meta.add_run("Academic Research Paper in Cryptography, Cybersecurity, and Blockchain Systems")
    r_m.font.name = 'Times New Roman'
    r_m.font.size = Pt(8.8)
    r_m.italic = True
    r_m.font.color.rgb = RGBColor(97, 97, 97)

    # ABSTRACT BOX
    tbl_abs = doc.add_table(rows=1, cols=1)
    tbl_abs.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_abs = tbl_abs.cell(0, 0)
    set_cell_background(cell_abs, "F0F4F8")
    set_cell_margins(cell_abs, top=40, bottom=40, left=70, right=70)
    
    p_abs = cell_abs.paragraphs[0]
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.space_before = Pt(0)
    p_abs.paragraph_format.space_after = Pt(0)
    p_abs.paragraph_format.line_spacing = 1.0
    r_ab_b = p_abs.add_run("Abstract— ")
    r_ab_b.bold = True
    r_ab_b.font.size = Pt(8.8)
    r_ab_t = p_abs.add_run(
        "The RSA algorithm remains a foundational pillar of modern public-key cryptography. "
        "While public blockchain consensus protocols predominantly utilize elliptic-curve cryptography (ECC) for on-chain state compactness, "
        "RSA plays an enduring role in enterprise infrastructure, Public Key Infrastructure (PKI), and internal gateway authorization. "
        "This report provides an academic investigation of real-world RSA applications across theory, operational justification, and systems engineering. "
        "We formulate RSA's mathematical foundations, contrasting RSA-OAEP key transport with RSA-PSS digital signatures (WHAT). "
        "We analyze why RSA is favored in specific trust architectures, providing an evidence-based comparison against ECDSA and Schnorr signatures (WHY). "
        "Finally, we design, implement, and benchmark an educational off-chain cryptocurrency withdrawal authentication system using RSA-PSS and SHA-256 (HOW). "
        f"Empirical benchmarks across RSA (2048, 3072, 4096 bits) and ECDSA (secp256k1) on identical hardware demonstrate RSA's distinct operational profile: "
        f"while RSA signing is slower than ECDSA, RSA public exponent verification (e = 65,537) executes significantly faster across all tested key sizes—"
        f"RSA-2048 is {ratio_2048_ec}x faster, RSA-3072 is {ratio_3072_ec}x faster, and RSA-4096 is {ratio_4096_ec}x faster than ECDSA verification. "
        f"At the approximately equivalent 128-bit classical security level (RSA-3072 vs. ECDSA-secp256k1), RSA-3072 verification is {ratio_3072_ec}x faster than ECDSA, "
        f"whereas ECDSA signing is {ratio_sign_ec}x faster than RSA-3072. "
        "Adversarial security scenario testing demonstrates that combining cryptographic digital signatures with application-level timestamp freshness and nonce replay caches "
        "significantly strengthens request authentication against payload tampering and replay attacks, although complete system security requires defense-in-depth "
        "across transport encryption, secure key custody, and operational controls. "
        "Evaluation against the bundled RSA-PSS 2048-bit SHA-256/MGF1-SHA256 Wycheproof test-vector set (version 0.9 snapshot, 108 cases) confirms that the verification engine "
        "correctly accepts all 63 expected-valid test cases and rejects all 45 expected-invalid test cases, validating execution against this selected verification suite."
    )
    r_ab_t.font.size = Pt(8.8)

    p_kw = add_p(space_before=1.0, space_after=1.5)
    r_kw_b = p_kw.add_run("Keywords: ")
    r_kw_b.bold = True
    r_kw_b.font.size = Pt(8.3)
    r_kw = p_kw.add_run("RSA Cryptography, RSA-PSS, Digital Signatures, PKI, Hybrid Encryption, Cryptocurrency Security, Off-chain Authentication, Empirical Evaluation.")
    r_kw.font.size = Pt(8.3)
    r_kw.italic = True

    # -------------------------------------------------------------
    # SECTION 1: INTRODUCTION AND RESEARCH SCOPE
    # -------------------------------------------------------------
    add_h1("1. Introduction and Research Scope")
    p = add_p()
    p.add_run(
        "First documented by Ron Rivest, Adi Shamir, and Leonard Adleman in their April 1977 MIT research memorandum and published in Communications of the ACM in 1978 [1], "
        "and formally standardized under PKCS #1 / RFC 8017 [2], the RSA algorithm solved the historic key distribution problem "
        "by separating the private transformation used for decryption and signing from the public transformation used for encryption and verification. "
        "For nearly five decades, RSA has underpinned digital commerce, software distribution, and enterprise identity management."
    )
    p = add_p()
    p.add_run(
        "In modern blockchain environments, significant architectural debate centers on algorithm selection. Major public networks—including Bitcoin and Ethereum—rely "
        "on Elliptic Curve Cryptography (ECC) for native on-chain transaction signatures [8], [12], [13]. In enterprise cryptocurrency operations, transaction handling does not occur solely on-chain; "
        "systems may employ layered off-chain microservices, secure hardware enclaves or Hardware Security Modules (HSMs), and Transport Layer Security (TLS 1.3) tunnels [3] "
        "to authenticate and authorize requests before dispatching them to blockchain nodes. This report investigates real-world RSA applications across three dimensions: "
        "(1) WHAT: mathematical principles and operational distinctions between RSA-OAEP key transport and RSA-PSS signatures; "
        "(2) WHY: security justification of RSA and an evidence-based comparison with ECDSA and Schnorr; "
        "(3) HOW: practical design, implementation, and empirical evaluation of an educational off-chain cryptocurrency withdrawal authentication system using RSA-PSS."
    )

    # -------------------------------------------------------------
    # SECTION 2: RSA FUNDAMENTALS AND REAL-WORLD APPLICATIONS
    # -------------------------------------------------------------
    add_h1("2. RSA Fundamentals and Real-World Applications")
    add_h2("2.1 Mathematical Foundations and Operating Mechanics")
    p = add_p()
    p.add_run(
        "The security of RSA rests on the integer factorization problem—the computational difficulty of determining prime factors p and q from modulus n = p · q [1], [2]. "
        "The operational lifecycle comprises: (i) computing Euler's totient φ(n) = (p − 1)(q − 1); (ii) selecting public exponent e coprime to φ(n) "
        "(standardized as Fermat prime e = 65,537 = 2¹⁶ + 1); and (iii) deriving private exponent d ≡ e⁻¹ (mod φ(n)). "
        "The public key comprises (e, n), and the private key comprises (d, n) or Chinese Remainder Theorem (CRT) parameters (p, q, dP, dQ, qInv). "
        "By Euler's theorem, for any message m coprime to n, m^(e·d) ≡ m (mod n). "
        "Textbook RSA operates directly on integers (c = m^e mod n; m = c^d mod n), but is vulnerable to algebraic homomorphic manipulation and chosen-ciphertext attacks. "
        "Secure real-world implementations mandate modern randomized padding schemes."
    )

    add_h2("2.2 Distinction Between RSA Encryption and RSA Digital Signatures")
    p = add_p()
    p.add_run(
        "RSA supports two distinct operational primitives designed for contrasting security goals:\n"
        "• Asymmetric Encryption (Confidentiality): The sender encrypts plaintext using recipient public key (e, n); only private key d can decrypt. "
        "Modern systems employ RSA-OAEP (RFC 8017 Section 7.1 [2]). In the Random Oracle Model (ROM), Bellare and Rogaway (1994) [17] introduced OAEP and established semantic security against chosen-plaintext attacks (IND-CPA) and plaintext awareness (implying IND-CCA1 security for general trapdoor permutations). "
        "Subsequently, Shoup (2001) [15] demonstrated that the general IND-CCA2 security proof claim could not be established for arbitrary trapdoor permutations via standard black-box reductions, identified the critical relevance of partial-domain one-wayness, and proposed the provably secure variant OAEP+. "
        "Fujisaki, Okamoto, Pointcheval, and Stern (2001) [16] established IND-CCA2 security specifically for RSA-OAEP in the ROM under the standard RSA one-wayness assumption by proving that partial-domain one-wayness is mathematically equivalent to full-domain one-wayness for the RSA permutation, though the concrete security reduction is non-tight for practical RSA key lengths. "
        "Because RSAES-OAEP payload size is bounded by mLen <= k - 2hLen - 2 (RFC 8017 Section 7.1.1; 190 bytes for RSA-2048 with SHA-256), "
        "industrial architectures deploy it within hybrid encryption for RSA key transport—encapsulating ephemeral symmetric keys (e.g., 256-bit AES-GCM per NIST SP 800-56B Rev. 2 [5]) "
        "to secure high-throughput bulk data streaming.\n"
        "• Digital Signatures (Authenticity, Integrity, Non-Repudiation Evidence): Under RFC 8017 Section 8.1 / 9.1 and NIST FIPS 186-5 [2], [4], RSA-PSS is the state-of-the-art standard. "
        "Given original message octet string M, the signing sequence computes message digest mHash = Hash(M), generates encoded message octet string EM = EMSA-PSS-ENCODE(M, emBits = modBits − 1) incorporating a randomized salt, converts octets to integer message representative m = OS2IP(EM), computes signature representative s = RSASP1(SK, m) (via private exponent d or CRT parameters), and formats signature octet string S = I2OSP(s, k). "
        "The verifier parses integer s = OS2IP(S), applies public modular exponentiation to recover integer representative m = RSAVP1(PK, s) = s^e mod n, converts integer to octet string EM = I2OSP(m, emLen), and executes EMSA-PSS-VERIFY(M, EM, emBits). "
        "Crucially, modular exponentiation (RSAVP1) alone does not establish signature validity; EMSA-PSS decoding—unmasking the randomized salt via MGF1, checking padding bytes, and confirming hash consistency against M—is indispensable. "
        "PSS achieves a tight security reduction to the RSA problem in the ROM (EUF-CMA). Cryptographic signatures furnish non-repudiation evidence, while full non-repudiation requires identity binding, secure custody, and operational controls.\n"
        "• Cryptographic Key Separation (NIST FIPS 186-5 Section 5.1 / SP 800-57): A vital security mandate in asymmetric cryptography is strict key separation. "
        "NIST FIPS 186-5 Section 5.1 explicitly dictates that an RSA key pair designated for digital signatures shall not be used for any other purpose, such as key establishment or encryption (RSA-OAEP). "
        "Multi-purpose key reuse exposes systems to cross-protocol interaction attacks, undermines non-repudiation auditing, and expands compromise blast radius. "
        "Architectures deploying both signing and key transport must enforce separate key pairs, distinct certificate bindings, and independent key-management policies."
    )

    # Figure 1: RSA-PSS Workflow
    wf_img = FIG_DIR / "rsa_pss_workflow.png"
    if wf_img.exists():
        p_img = add_p(space_before=0.8, space_after=0.4, align=WD_ALIGN_PARAGRAPH.CENTER)
        p_img.paragraph_format.keep_with_next = True
        r_img = p_img.add_run()
        r_img.add_picture(str(wf_img), width=Inches(3.85))
        p_cap = add_p(space_before=0.4, space_after=1.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run("Figure 1. Operational workflow of the RSA-PSS probabilistic digital signature scheme (RFC 8017 / FIPS 186-5).")
        r_cap.font.size = Pt(7.8)
        r_cap.italic = True

    add_h2("2.3 Real-World Application Breadth")
    p = add_p()
    p.add_run(
        "In industrial systems, RSA is deployed across three primary domains: "
        "(1) Hybrid Encryption and RSA Key Transport: RSA is not used to encrypt bulk data directly due to algebraic length constraints: under RFC 8017 Section 7.1.1 [2], "
        "plaintext size for RSA-OAEP is bounded by mLen <= k - 2hLen - 2 (190 bytes for RSA-2048 with SHA-256). "
        "Instead, RSA-OAEP is deployed for RSA key transport—encapsulating ephemeral symmetric keys (e.g., 256-bit AES-GCM per NIST SP 800-56B Rev. 2 [5])—combining asymmetric key establishment with high-throughput symmetric streaming. "
        "(2) Code Signing and Firmware Integrity: Operating systems, application marketplaces, and secure bootloaders frequently deploy RSA digital signatures (including RSA-PSS and PKCS#1 v1.5) to verify executable integrity before launch. "
        "(3) Digital Certificates and PKI: In TLS 1.3 (RFC 9846 [3], superseding RFC 8446), static RSA key exchange was entirely removed in favor of ephemeral Diffie-Hellman ((EC)DHE) and PSK-DHE (psk_dhe_ke) to guarantee forward secrecy. "
        "In contrast, PSK-only mode (psk_ke) does not provide forward secrecy against compromised pre-shared keys, and 0-RTT early data lacks forward secrecy and is vulnerable to replay attacks. "
        "Post-quantum forward secrecy additionally requires negotiating a supported hybrid mechanism (e.g., RFC 10024). "
        "Thus, RSA's modern TLS 1.3 role is strictly endpoint authentication: RSA X.509 certificates authenticate servers via RSA-PSS CertificateVerify messages (RFC 9846), while RFC 9963 provides a restricted legacy exception for client authentication with PKCS#1 v1.5 in constrained environments."
    )

    # -------------------------------------------------------------
    # SECTION 3: WHY RSA? SECURITY PURPOSE AND COMPARISON
    # -------------------------------------------------------------
    add_h1("3. Why RSA? Security Purpose and Comparative Evaluation")
    p = add_p()
    p.add_run(
        "RSA addresses the core security objectives of information assurance: confidentiality (via hybrid key transport), entity authentication, "
        "data integrity, and non-repudiation evidence. Table 1 compares RSA with elliptic curve alternatives: "
        "ECDSA (secp256k1) [12], [13], Schnorr (BIP 340) [8], and Ed25519 [11], with security strengths benchmarked according to NIST SP 800-56B Rev. 2 (Table 2 and Appendix D) [5] "
        "and generic elliptic-curve strength mappings from NIST SP 800-57 Part 1 Rev. 5 [6]."
    )

    # TABLE 1: COMPARISON TABLE
    tbl_comp = doc.add_table(rows=5, cols=6)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_comp)

    headers = ["Evaluation Metric", "RSA-2048", "RSA-3072", "ECDSA (secp256k1)", "Schnorr (BIP 340)", "Ed25519 (RFC 8032)"]
    for j, h in enumerate(headers):
        cell = tbl_comp.cell(0, j)
        set_cell_background(cell, "E8EAF6")
        set_cell_margins(cell, top=16, bottom=16, left=25, right=25)
        p_c = cell.paragraphs[0]
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.paragraph_format.space_before = Pt(0)
        p_c.paragraph_format.space_after = Pt(0)
        r = p_c.add_run(h)
        r.bold = True
        r.font.size = Pt(7.6)

    comp_data = [
        ["Hard Problem", "Factoring", "Factoring", "EC Discrete Log", "EC Discrete Log", "Edwards EC-DLOG"],
        ["Security Strength", "112 bits [5]", "128 bits [5]", "~128 bits (generic EC mapping [6])", "128 bits (generic EC mapping [6])", "128 bits (generic EC mapping [6])"],
        ["Key Size / Sig Size", 
         "Modulus: 256 B\nSig: 256 B\nDER PubKey: ~294 B", 
         "Modulus: 384 B\nSig: 384 B\nDER PubKey: ~422 B", 
         "PubKey: 33 B (comp)\nBitcoin: 70–72 B (71 B sample)\nEthereum: 65 B (r||s||v), RLP; 64 B (ERC-2098)", 
         "PubKey: 32 B (x-only)\nBIP341: 64 B (DEFAULT)\nor 65 B (explicit sighash)", 
         "PubKey: 32 B\nSig: 64 B [11]"],
        ["Relative Verify Speed", 
         f"Empirical: {r2048_ver_ms:.3f} ms\n({ratio_2048_ec}x vs ECDSA)", 
         f"Empirical: {r3072_ver_ms:.3f} ms\n({ratio_3072_ec}x vs ECDSA)", 
         f"Empirical: {ecdsa_ver_ms:.3f} ms\n(Baseline: 1.0x)", 
         "Batch verify supported;\nnot benchmarked [8]", 
         "High efficiency in lit. [11];\nnot benchmarked"],
    ]

    for i, row in enumerate(comp_data):
        for j, val in enumerate(row):
            cell = tbl_comp.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(cell, "F9FAFB")
            set_cell_margins(cell, top=14, bottom=14, left=25, right=25)
            p_c = cell.paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            p_c.paragraph_format.space_before = Pt(0)
            p_c.paragraph_format.space_after = Pt(0)
            r = p_c.add_run(val)
            r.font.size = Pt(7.4)

    p_tc = add_p(space_before=1, space_after=1.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_tc.paragraph_format.keep_with_next = True
    r_tc = p_tc.add_run("Table 1. Systematic comparison of asymmetric cryptographic algorithms across security and operational metrics.")
    r_tc.font.size = Pt(7.8)
    r_tc.italic = True

    add_h2("3.1 Storage and Verification Trade-Offs in Blockchain Consensus Layers")
    p = add_p()
    p.add_run(
        "A central requirement of public blockchains is minimizing ledger bloat and bandwidth overhead. "
        "In Bitcoin and Ethereum, transaction fees and execution costs penalize excessive data footprints. "
        "Under Bitcoin's economic model, fees equal transaction virtual size (vSize in vB) multiplied by prevailing feerate (sat/vB), "
        "whereas Ethereum costs are measured in gas for execution steps and calldata serialization [12], [13]. "
        "In both networks, compact signatures and public keys are paramount for throughput and decentralized state validation. "
        "To evaluate transaction overhead accurately under Bitcoin BIP 141 (Segregated Witness) [9], transaction weight is formulated as "
        "Weight = (Base Size * 3) + Total Size, and virtual size is vSize = ceil(Weight / 4). "
        "A standard 1-input, 2-output SegWit P2WPKH transaction has a baseline virtual size of ~141 vB (~210–220 serialized bytes). "
        "For a typical P2WPKH witness stack—comprising 1 byte for stack item count, 1 byte for signature length prefix, ~70–72 bytes for the DER signature plus sighash byte, "
        "1 byte for public key length prefix, and 33 bytes for the compressed public key—the witness totals approximately 107–109 bytes [12]. "
        "In a hypothetical architecture where RSA-2048 were used for native transaction authorization, explicitly assuming two separate stack items "
        "(a 256-byte RSA modulus and a 256-byte RSA signature, each prefixed by a 3-byte CompactSize length prefix for 256-byte items), "
        "the witness size equals 1 + 3 + 256 + 3 + 256 = 519 bytes. Compared with standard P2WPKH, this adds approximately 410–412 witness bytes per input. "
        "Under BIP 141 weight rules, this witness overhead adds 410–412 weight units, which corresponds to approximately 103 additional virtual bytes "
        "(~103 vB per input, subject to transaction weight rounding). For a representative baseline 141-vB transaction, this hypothetical expansion is "
        "approximately 73% (expanding to ~244 vB), proportionally increasing miner fees. "
        "Crucially, this analysis models a hypothetical transaction format; native Bitcoin RSA verification is not supported "
        "(Bitcoin script lacks native RSA verification opcodes, requiring consensus hard or soft forks), and the 73% expansion assumes both RSA values "
        "are carried in each input. Alternative key-storage designs—such as registering public keys in an on-chain key directory, smart-contract registry, "
        "or referencing them via script hashes—would substantially alter and reduce this overhead. "
        "Similarly, native Ethereum Externally Owned Account (EOA) transaction authorization mandates ECDSA over secp256k1 [13]. "
        "In network-level transaction envelopes (legacy, EIP-2930, and EIP-1559), Ethereum serializes signatures as discrete Recursive Length Prefix (RLP) fields "
        "encoding r, s, and v (or yParity for typed envelopes). While off-chain systems commonly concatenate these into a 65-byte r||s||v string, "
        "ERC-2098 also defines a compact 64-byte representation that packs yParity into the upper bit of s. "
        "While Ethereum smart contracts can execute raw modular exponentiation via the EVM precompile at address 0x05 (EIP-198), "
        "this precompile computes B^E mod M only; complete RSA-PSS verification additionally requires separate contract bytecode to execute MGF1 mask generation, "
        "extract the encoded message, and validate hash/padding integrity. For native transaction envelopes, consensus rules strictly require ECC. "
        "In contrast, BIP 340 Schnorr signatures over secp256k1 integrated via BIP 341 (Taproot) are exactly 64 bytes under SIGHASH_DEFAULT "
        "(or 65 bytes when an explicit non-default sighash byte is appended), paired with 32-byte x-only public keys, and enable two-round multi-signature "
        "aggregation via MuSig2 (BIP 327 [10]), allowing n-of-n signers to publish a single compact 64-byte signature on-chain—a capability unattainable with standard RSA."
    )

    add_h2("3.2 The Operational Value of RSA in Off-Chain Systems")
    p = add_p(space_before=0, space_after=0.2, line_spacing=1.0)
    p.add_run(
        "Despite on-chain limitations, RSA provides distinct benefits in off-chain exchange backends: "
        "(1) Asymmetric Verification Speed: RSA public exponentiation with e = 65,537 = 2¹⁶ + 1 = 10000000000000001₂ (17 bits, Hamming weight 2) requires only 16 modular squarings "
        "and 1 modular multiplication under straightforward square-and-multiply exponentiation (17 operations total), enabling rapid verification at edge gateways. "
        "(2) Hardware Security Module (HSM) Integration: Enterprise banking infrastructure and secure enclaves feature mature hardware support for RSA modular arithmetic. "
        "(3) Avoidance of Scalar Nonce Reuse Hazards: Standard ECDSA is fragile against nonce failure: if the signing nonce k repeats or exhibits slight bit bias, "
        "the private key is algebraically exposed. While RSA-PSS eliminates scalar nonce leakage, it does not remove all side-channel risks: "
        "implementations must employ base blinding (randomizing the base integer with a secret factor r: x' = x · r^e mod n) to mitigate timing side channels. "
        "Crucially, blinding alone does not prevent hardware fault injection such as the Bellcore attack on Chinese Remainder Theorem (CRT) implementations (Boneh et al. [7]). "
        "In CRT signing, the signer computes s_p = m^(d_p) mod p and s_q = m^(d_q) mod q, where m = OS2IP(EM) is the integer message representative from EMSA-PSS-ENCODE(M) (RFC 8017 Section 8.1 / 9.1 [2]), satisfying s^e ≡ m (mod n). "
        "Bellcore fault attacks operate under two distinct formulations:\n"
        "• Two-Signature Formulation: Requires one correct signature s and one faulty signature s' generated from the exact same representative m = OS2IP(EM). "
        "If a fault corrupts s_q into s'_q while s_p is uncorrupted, s' satisfies s' ≡ s (mod p) and s' ≢ s (mod q), yielding gcd(s − s', n) = p (or q if s_p is faulted); thus gcd(s − s', n) ∈ {p, q}. "
        "Crucially, because RSA-PSS randomizes the salt, independent signing runs on message M produce differing encodings (EM₁ ≠ EM₂) and representatives (m₁ ≠ m₂); two signatures with differing salts do not satisfy this condition.\n"
        "• Single-Fault Formulation: An attacker knowing the exact representative m of faulty signature s' factors n via gcd((s')^e − m, n) ∈ {p, q}. "
        "This assumes knowledge of the exact encoded representative m of that specific execution, not merely application message M. "
        "While any valid signature reveals its own representative via s^e mod n, it does not reveal the representative of an independently salted faulty execution.\n"
        "Countermeasures must remain strictly differentiated: (i) Base blinding mitigates timing side channels, NOT CRT faults; "
        "(ii) CRT fault defense requires post-computation verification—verifying m_check = (s^e mod n) against m = OS2IP(EM) and checking EMSA-PSS consistency before releasing s—or (iii) redundant fault-detection hardware."
    )

    # -------------------------------------------------------------
    # SECTION 4: PROPOSED SYSTEM DESIGN AND IMPLEMENTATION
    # -------------------------------------------------------------
    add_h1("4. Proposed System Design and Implementation")
    p = add_p(space_before=0, space_after=0.2, line_spacing=1.0)
    p.add_run(
        "We design and evaluate an educational, off-chain architecture: Using RSA-PSS Digital Signatures to Authenticate Off-Chain Withdrawal Requests in Cryptocurrency Exchanges. "
        "Important Technical Boundary: The proposed educational architecture operates strictly off-chain within an internal authorization boundary to authenticate withdrawal requests "
        "before they reach hot-wallet signers; it does not replace on-chain ECDSA/Schnorr consensus signatures on Bitcoin or Ethereum, nor does it represent the proprietary architecture "
        "of any specific commercial exchange."
    )

    add_h2("4.1 Architecture and Component Decomposition")
    p = add_p(space_before=0, space_after=0.2, line_spacing=1.0)
    p.add_run(
        "As illustrated in Figure 2, the authentication pipeline decouples request origination from on-chain broadcast across four components:\n"
        "1. Withdrawal Service (Client/Frontend): Formats the withdrawal request: blockchain network, recipient address, withdrawal amount (in exact integer atomic units, e.g., wei), a UUIDv4 nonce, and a UNIX epoch timestamp.\n"
        "2. RSA Signing Component: Encapsulated within a secure enclave or signing service. It formats the payload using deterministic JSON serialization, computes the SHA-256 digest, and signs via RSA-PSS using the exchange private key.\n"
        "3. Verification Service: An edge gateway that extracts the exchange RSA public key, reconstructs the message digest, and validates the PSS signature.\n"
        "4. Request Validation Engine: Enforces stateful application rules: evaluates timestamp freshness (±300s skew) and checks nonce uniqueness against a replay cache."
    )

    # Figure 2: Architecture Diagram
    arch_img = FIG_DIR / "withdrawal_architecture.png"
    if arch_img.exists():
        p_img = add_p(space_before=0.4, space_after=0.2, align=WD_ALIGN_PARAGRAPH.CENTER)
        p_img.paragraph_format.keep_with_next = True
        r_img = p_img.add_run()
        r_img.add_picture(str(arch_img), width=Inches(1.85))
        p_cap = add_p(space_before=0.2, space_after=0.6, align=WD_ALIGN_PARAGRAPH.CENTER)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run("Figure 2. Proposed off-chain cryptocurrency withdrawal authentication architecture using RSA-PSS.")
        r_cap.font.size = Pt(7.8)
        r_cap.italic = True

    p_h42 = add_h2("4.2 Deterministic JSON Serialization and Pipeline Algorithm")
    p_h42.paragraph_format.page_break_before = True
    p = add_p(space_before=0, space_after=0.2, line_spacing=1.0)
    p.add_run(
        "Cryptographic signature verification fails if distributed microservices serialize JSON keys or whitespace inconsistently. "
        "Our system implements deterministic JSON serialization (sorting dictionary keys lexicographically, eliminating whitespace, and encoding to UTF-8). "
        "Note: While inspired by canonical formatting, this custom serialization does not implement full RFC 8785 (which requires ECMAScript number formatting and UTF-16 code unit ordering); "
        "it provides deterministic byte-level consistency for the defined data schema. "
        "Per RFC 8017 Section 9.1, EMSA-PSS encoding specifies emBits = modBits − 1 to ensure that the encoded message representative m = OS2IP(EM) satisfies m < n. "
        "For a 2048-bit modulus (modBits = 2048), emBits = 2047 bits and emLen = ceil(emBits / 8) = 256 bytes, with salt length constrained by sLen <= emLen − hLen − 2 "
        "(for SHA-256 hLen = 32, sLen <= 222 bytes; our pipeline deploys sLen = 32 bytes). Algorithm 1 details the complete lifecycle."
    )

    # Algorithm 1 Box (Kept intact with cantSplit and keep_together)
    tbl_code = doc.add_table(rows=1, cols=1)
    tbl_code.alignment = WD_TABLE_ALIGNMENT.CENTER
    trPr = tbl_code.rows[0]._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    cell_code = tbl_code.cell(0, 0)
    set_cell_background(cell_code, "F8F9FA")
    set_cell_margins(cell_code, top=8, bottom=8, left=25, right=25)
    p_code = cell_code.paragraphs[0]
    p_code.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(0)
    p_code.paragraph_format.line_spacing = 1.0
    p_code.paragraph_format.keep_together = True
    r_code = p_code.add_run(
        "Algorithm 1: Off-Chain Withdrawal Authentication Pipeline\n"
        "Input:  Request R = {id, net, addr, amt_atomic, nonce, ts}, Private Key SK_rsa, Public Key PK_rsa\n"
        "Output: Decision ∈ {ACCEPT, REJECT_SIG, REJECT_REPLAY, REJECT_EXPIRED}\n"
        "1:  M_canon ← DeterministicJSON(R)                      // Lexicographical keys, compact separators, UTF-8\n"
        "2:  EM ← EMSA-PSS-ENCODE(M_canon, emBits=modBits−1, sLen=32) // RFC 8017 PSS encoding\n"
        "3:  σ ← RSASP1(SK_rsa, OS2IP(EM))                       // Signature generation\n"
        "4:  // Gateway Verification Phase\n"
        "5:  valid_sig ← RSASSA-PSS-Verify(PK_rsa, M_canon, σ, SHA-256, sLen=32)\n"
        "6:  if ¬ valid_sig then return REJECT_SIG                 // Tampering detected\n"
        "7:  if |CurrentTime() − R.ts| > Δ_skew then return REJECT_EXPIRED\n"
        "8:  if R.nonce ∈ NonceStore then return REJECT_REPLAY     // Replay detected\n"
        "9:  NonceStore.Add(R.nonce); return ACCEPT"
    )
    r_code.font.name = 'Consolas'
    r_code.font.size = Pt(7.0)

    add_h2("4.3 Prototype Scope and Vital Security Considerations")
    p = add_p(space_before=0, space_after=0.2, line_spacing=1.0)
    p.add_run(
        "To maintain academic defensibility, the prototype implementation scope must be clearly delineated from production requirements: "
        "(1) Stateful Replay Prevention: The prototype verifies and stores nonces in an in-memory Python set. While appropriate for an educational prototype, an in-memory set is not sufficient for distributed production replay prevention. Under concurrent requests, nonce verification and consumption must be strictly atomic (e.g., via Redis SETNX or SQL transactional INSERT with unique constraints) to avoid time-of-check-to-time-of-use (TOCTOU) race conditions, backed by a persistent datastore with TTL expiry that persists across horizontal microservice restarts. "
        "(2) Address and Validation Logic: Address checking is a prototype-level format sanity check (verifying 0x hex prefix and length), whereas production gateways require full checksum validation (EIP-55 for Ethereum, Bech32/Bech32m for Bitcoin) alongside business-tier balance checks, withdrawal thresholds, and AML screening. "
        "(3) Serialization Scope: The payload serializer applies deterministic key sorting and compact UTF-8 encoding; it does not implement full RFC 8785 (JCS) compliance. "
        "(4) Key Lifecycle and Trust: The verifier operates on pre-provisioned trusted public keys without a complete PKI, automated certificate path validation, revocation (CRLs/OCSP), or automated key rotation. "
        "(5) Key Custody: Signing private keys reside in process memory for educational demonstration, whereas production gateways deploy appropriately validated HSMs or secure hardware—preferring active FIPS 140-3 validated modules for new procurements, while recognizing legacy FIPS 140-2 modules (transitioned to the NIST CMVP Historical List in September 2026) for existing systems—based on the operational threat model, regulatory environment, and institutional key-management policies."
    )

    # -------------------------------------------------------------
    # SECTION 5: EXPERIMENTAL RESULTS AND ANALYSIS
    # -------------------------------------------------------------
    add_h1("5. Experimental Results and Analysis")
    p = add_p(space_before=0, space_after=0.2, line_spacing=1.0)
    p.add_run(
        "The system was implemented in Python 3.15 using the cryptography library (v50.0.2) backed by OpenSSL 4.0.3. "
        "Experiments were executed on an AMD Ryzen 5 7520U processor (4 cores, 8 threads @ 2.80 GHz) running Windows 11 Build 26200. "
        "High-resolution timings were captured using time.perf_counter_ns() across 10 key generation trials and 100 signature generation and verification trials. "
        "Both RSA (2048, 3072, 4096 bits) and ECDSA (secp256k1) were benchmarked independently under identical conditions."
    )

    add_h2("5.1 Adversarial Security Testing Scenarios")
    p = add_p(space_before=0, space_after=0.2, line_spacing=1.0)
    p.add_run(
        "Execution of rsa_pss_experiment.py validated all five target security scenarios: "
        "(1) Scenario 1 (Valid Request): Authentic request (12.5 ETH in atomic units) verified and validated -> Outcome: ACCEPTED; "
        "(2) Scenario 2 (Tampered Amount): Amount modified to 50.0 ETH equivalent; signature verification returned False -> Outcome: REJECTED; "
        "(3) Scenario 3 (Tampered Recipient): Address modified to attacker account; verification returned False -> Outcome: REJECTED; "
        "(4) Scenario 4 (Rogue Public Key): Signature evaluated against an unauthorized RSA public key -> Outcome: REJECTED; "
        "(5) Scenario 5 (Replay Attack): Identical request resubmitted; cryptographic signature verified (True), but duplicate nonce 'a8f9c10e-8215-4c07-b649-1d2e3f4a5b6c' was intercepted -> Outcome: REJECTED BY APPLICATION STATE ENGINE."
    )

    add_h2("5.2 Bundled Wycheproof Test Suite Validation")
    p = add_p(space_before=0, space_after=0.2, line_spacing=1.0)
    p.add_run(
        "To evaluate implementation compliance against authoritative test vectors, our test harness loaded and executed the bundled "
        "RSA-PSS 2048-bit SHA-256/MGF1-SHA256 Wycheproof test-vector set (version 0.9 snapshot, 108 cases) (rsa_pss_2048_sha256_mgf1_32_test.json) [14]. "
        "The suite comprises 108 test vectors: 63 expected-valid signatures and 45 expected-invalid signatures. "
        "Our verification engine successfully passed all 108 test cases (100% agreement, 0 failures), correctly accepting every valid signature "
        "and rejecting all corrupted or edge-case invalid signatures. This validates the implementation against the specific bundled Wycheproof test cases, "
        "representing a selected verification test set rather than exhaustive mathematical proof of all possible RFC 8017 edge cases. "
        "(The current upstream C2SP repository contains an expanded number of cases; the bundled v0.9 snapshot is preserved for experimental reproducibility)."
    )

    add_h2("5.3 Empirical Benchmarking and Performance Analysis")
    p = add_p(space_before=0, space_after=0.2, line_spacing=1.0)
    p.add_run(
        "Table 2 reports empirical benchmarks comparing RSA configurations with ECDSA (secp256k1). Figure 3 illustrates the median latency comparison."
    )

    # Table 2 Caption (Standard academic placement directly above table)
    p_b_cap = add_p(space_before=0.2, space_after=0.2, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_b_cap.paragraph_format.keep_with_next = True
    r_bc = p_b_cap.add_run("Table 2. Empirical benchmark measurements (AMD Ryzen 5 7520U, Python 3.15, OpenSSL 4.0.3, median of 10 keygen / 100 crypto trials).")
    r_bc.font.size = Pt(7.4)
    r_bc.italic = True

    # TABLE 2: BENCHMARK RESULTS (LOADED DIRECTLY FROM ACTIVE CSV)
    tbl_bench = doc.add_table(rows=5, cols=7)
    tbl_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_bench)
    for row_obj in tbl_bench.rows:
        trPr = row_obj._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    b_headers = ["Algorithm", "Security Level", "Keygen Median", "Sign Median", "Verify Median", "Sig Size", "Internal Asymmetry"]
    for j, h in enumerate(b_headers):
        cell = tbl_bench.cell(0, j)
        set_cell_background(cell, "E8EAF6")
        set_cell_margins(cell, top=5, bottom=5, left=12, right=12)
        p_c = cell.paragraphs[0]
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.paragraph_format.space_before = Pt(0)
        p_c.paragraph_format.space_after = Pt(0)
        r = p_c.add_run(h)
        r.bold = True
        r.font.size = Pt(7.2)

    bench_rows = [
        ["RSA-2048", f"{r2048['security_strength_bits']} bits [5]", f"{r2048['keygen_median_ms']} ms", f"{r2048['sign_median_ms']} ms", f"{r2048['verify_median_ms']} ms", f"{r2048['signature_length_bytes']} B", f"{r2048['internal_asymmetry_ratio']}x (Sign / Verify)"],
        ["RSA-3072", f"{r3072['security_strength_bits']} bits [5]", f"{r3072['keygen_median_ms']} ms", f"{r3072['sign_median_ms']} ms", f"{r3072['verify_median_ms']} ms", f"{r3072['signature_length_bytes']} B", f"{r3072['internal_asymmetry_ratio']}x (Sign / Verify)"],
        ["RSA-4096", f"{r4096['security_strength_bits']} bits [5]", f"{r4096['keygen_median_ms']} ms", f"{r4096['sign_median_ms']} ms", f"{r4096['verify_median_ms']} ms", f"{r4096['signature_length_bytes']} B", f"{r4096['internal_asymmetry_ratio']}x (Sign / Verify)"],
        ["ECDSA-secp256k1", f"~{ecdsa['security_strength_bits']} bits [6]", f"{ecdsa['keygen_median_ms']} ms", f"{ecdsa['sign_median_ms']} ms", f"{ecdsa['verify_median_ms']} ms", f"{ecdsa['signature_length_bytes']} B (DER sample)", f"{ecdsa['internal_asymmetry_ratio']}x (Sign / Verify)"]
    ]

    for i, row in enumerate(bench_rows):
        for j, val in enumerate(row):
            cell = tbl_bench.cell(i+1, j)
            if i % 2 == 1:
                set_cell_background(cell, "F9FAFB")
            set_cell_margins(cell, top=2.5, bottom=2.5, left=10, right=10)
            p_c = cell.paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_c.paragraph_format.space_before = Pt(0)
            p_c.paragraph_format.space_after = Pt(0)
            r = p_c.add_run(val)
            r.font.size = Pt(7.0)

    # Figure 3: Benchmark Chart
    bench_img = FIG_DIR / "benchmark_performance.png"
    if bench_img.exists():
        p_img = add_p(space_before=0.4, space_after=0.2, align=WD_ALIGN_PARAGRAPH.CENTER)
        p_img.paragraph_format.keep_with_next = True
        r_img = p_img.add_run()
        r_img.add_picture(str(bench_img), width=Inches(2.25))
        p_cap = add_p(space_before=0.2, space_after=0.3, align=WD_ALIGN_PARAGRAPH.CENTER)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run("Figure 3. Empirical median latency comparison for RSA and ECDSA key generation, signing, and verification.")
        r_cap.font.size = Pt(7.8)
        r_cap.italic = True

    p = add_p(space_before=0, space_after=0.4, line_spacing=1.01)
    p.add_run(
        "The empirical measurements demonstrate three decisive performance characteristics:\n"
        f"1. RSA Asymmetric Cost Structure: RSA displays a pronounced internal asymmetry: verification is {r2048['internal_asymmetry_ratio']}x (RSA-2048) to {r4096['internal_asymmetry_ratio']}x (RSA-4096) faster than its own signing operation. "
        "Because public exponent e = 65,537 = 2¹⁶ + 1 contains only two non-zero bits (10000000000000001₂), straightforward square-and-multiply exponentiation executes in 16 squarings and 1 multiplication (17 operations total), whereas private exponent d requires full modular exponentiation.\n"
        f"2. Head-to-Head Comparison with ECDSA: Comparing equivalent 128-bit classical security levels (RSA-3072 vs. ECDSA-secp256k1), ECDSA signing is {ratio_sign_ec}x faster than RSA signing ({ecdsa['sign_median_ms']} ms vs {r3072['sign_median_ms']} ms), "
        f"and ECDSA key generation is over {ratio_kg_ec}x faster ({ecdsa['keygen_median_ms']} ms vs {r3072['keygen_median_ms']} ms). Conversely, RSA-3072 signature verification ({r3072['verify_median_ms']} ms) is {ratio_3072_ec}x faster than ECDSA verification ({ecdsa['verify_median_ms']} ms). "
        f"While RSA-2048 verification ({r2048['verify_median_ms']} ms) is {ratio_2048_ec}x faster and RSA-4096 ({r4096['verify_median_ms']} ms) is {ratio_4096_ec}x faster than ECDSA, these represent 112-bit and 152-bit security levels rather than equivalent-strength comparisons. "
        "The recorded ECDSA DER signature sample was 71 bytes, with DER-encoded signatures generally varying between 70 and 72 bytes due to variable-length ASN.1 INTEGER encoding of r and s. "
        "These performance ratios are specific to the measured Python 3.15 / OpenSSL 4.0.3 execution environment on the AMD Ryzen 5 7520U processor; relative performance may vary across different CPU instruction sets (such as AVX-512) and compiled cryptographic libraries.\n"
        f"3. Isolated Operation Latency vs Gateway Throughput: At {r3072['verify_median_ms']} ms per verification, a single CPU core can theoretically evaluate ~{int(1000/r3072_ver_ms):,d} RSA-3072 signatures per second (vs ~{int(1000/ecdsa_ver_ms):,d} for ECDSA). "
        "Crucially, these figures represent isolated cryptographic operation timings, not an end-to-end exchange gateway throughput benchmark; real-world system throughput is bounded by network I/O, database persistence, and TLS handshakes."
    )

    # -------------------------------------------------------------
    # SECTION 6: CONCLUSION
    # -------------------------------------------------------------
    p_h6 = add_p(space_before=1.0, space_after=0.2, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.LEFT)
    p_h6.paragraph_format.keep_with_next = True
    r_h6 = p_h6.add_run("6. Conclusion")
    r_h6.bold = True
    r_h6.font.name = 'Times New Roman'
    r_h6.font.size = Pt(11.0)
    r_h6.font.color.rgb = RGBColor(26, 35, 126)

    p = add_p(space_before=0, space_after=0.2, line_spacing=1.0)
    p.add_run(
        "This research examined the cryptographic foundations, operational trade-offs, and practical deployment of RSA in modern security architectures. "
        "While elliptic-curve cryptography (ECDSA and Schnorr) rightfully dominates public blockchain consensus layers due to compact public keys and signatures that "
        "minimize transaction virtual size (reducing Bitcoin miner fees) and storage serialization (reducing Ethereum transaction execution and data gas overhead), "
        "RSA is not universally superior or inferior to ECC; rather, each algorithm serves distinct architectural domains. "
        "RSA remains a supported and deployed cryptographic option in enterprise PKI and can be deployed in selected off-chain authentication systems, "
        "particularly where existing infrastructure, interoperability, and asymmetric verification throughput are advantageous. "
        "Our prototype implementation of an off-chain withdrawal authentication system confirmed that RSA-PSS with SHA-256 provides verifiable message integrity with rapid gateway verification. "
        "However, cryptographic digital signatures alone do not guarantee complete system security; robust authorization requires defense-in-depth across deterministic serialization, "
        "stateful replay prevention, secure key custody (such as HSM storage), and transport encryption (TLS 1.3)."
    )
    p = add_p(space_before=0, space_after=0.2, line_spacing=1.0)
    p.add_run(
        "At an approximately equivalent 128-bit classical security strength, RSA-3072 provides robust resistance against conventional mathematical cryptanalysis, "
        "though it incurs substantially larger key and signature footprints than 256-bit elliptic curves. "
        "Looking toward future cryptographic horizons, RSA-PSS is vulnerable to polynomial-time integer factorization via Shor's algorithm on fault-tolerant quantum computers, "
        "as is standard elliptic-curve cryptography under discrete logarithm quantum attacks. Neither algorithm provides post-quantum security. "
        "Consequently, organizations deploying RSA-3072 today must maintain crypto-agility and actively prepare migration pathways toward standardized post-quantum digital signature algorithms, "
        "including NIST FIPS 204 (ML-DSA) and FIPS 205 (SLH-DSA)."
    )

    # -------------------------------------------------------------
    # SECTION 7: REFERENCES
    # -------------------------------------------------------------
    p_h7 = add_p(space_before=1.0, space_after=0.2, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.LEFT)
    p_h7.paragraph_format.keep_with_next = True
    r_h7 = p_h7.add_run("7. References")
    r_h7.bold = True
    r_h7.font.name = 'Times New Roman'
    r_h7.font.size = Pt(11.0)
    r_h7.font.color.rgb = RGBColor(26, 35, 126)

    refs = [
        "[1] R. L. Rivest, A. Shamir, and L. Adleman, \"A method for obtaining digital signatures and public-key cryptosystems,\" Communications of the ACM, vol. 21, no. 2, pp. 120–126, Feb. 1978 (MIT/LCS/TM-82, Apr. 1977). https://doi.org/10.1145/359340.359342",
        "[2] K. Moriarty, B. Kaliski, J. Jonsson, and A. Rusch, \"PKCS #1: RSA Cryptography Specifications Version 2.2,\" RFC 8017, IETF, Nov. 2016. https://www.rfc-editor.org/rfc/rfc8017",
        "[3] E. Rescorla, \"The Transport Layer Security (TLS) Protocol Version 1.3,\" RFC 9846, IETF, July 2026. https://www.rfc-editor.org/rfc/rfc9846",
        "[4] National Institute of Standards and Technology (NIST), \"Digital Signature Standard (DSS),\" Federal Information Processing Standards Publication (FIPS) 186-5, Feb. 2023. https://doi.org/10.6028/NIST.FIPS.186-5",
        "[5] E. Barker, L. Chen, A. Roginsky, A. Vassilev, and R. Davis, \"Recommendation for Pair-Wise Key-Establishment Schemes Using Integer Factorization Cryptography,\" NIST Special Publication (SP) 800-56B Rev. 2, Mar. 2019. https://doi.org/10.6028/NIST.SP.800-56Br2",
        "[6] E. Barker, \"Recommendation for Key Management: Part 1 – General,\" NIST Special Publication (SP) 800-57 Part 1 Rev. 5, May 2020. https://doi.org/10.6028/NIST.SP.800-57pt1r5",
        "[7] D. Boneh, R. A. DeMillo, and R. J. Lipton, \"On the importance of eliminating errors in cryptographic computations,\" Journal of Cryptology, vol. 14, no. 2, pp. 101–119, 2001. https://doi.org/10.1007/s001450010016",
        "[8] P. Wuille, J. Nick, and T. Ruffing, \"Schnorr Signatures for secp256k1,\" Bitcoin Improvement Proposal (BIP) 340, Jan. 2020. https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki",
        "[9] E. Lombrozo, J. Lau, and P. Wuille, \"Segregated Witness (Consensus layer),\" Bitcoin Improvement Proposal (BIP) 141, Dec. 2015. https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki",
        "[10] J. Nick, T. Ruffing, and E. Jin, \"MuSig2 for BIP340-compatible Multi-Signatures,\" Bitcoin Improvement Proposal (BIP) 327, 2023. https://github.com/bitcoin/bips/blob/master/bip-0327.mediawiki",
        "[11] S. Josefsson and I. Liusvaara, \"Edwards-Curve Digital Signature Algorithm (EdDSA),\" RFC 8032, IETF, Jan. 2017. https://www.rfc-editor.org/rfc/rfc8032",
        "[12] Bitcoin Core Developers, \"Bitcoin Developer Guide: Transactions,\" Bitcoin Project, n.d. [Online; accessed 2026]. https://developer.bitcoin.org/devguide/transactions.html",
        "[13] Ethereum Foundation, \"Ethereum Developer Documentation: Transactions and Cryptographic Signatures,\" n.d. [Online; accessed 2026]. https://ethereum.org/en/developers/docs/transactions/",
        "[14] Google Security Research, \"Project Wycheproof: Cryptographic Test Vectors for Asymmetric Algorithms,\" GitHub repository (v0.9 snapshot), n.d. [Online; accessed 2026]. https://github.com/google/wycheproof",
        "[15] V. Shoup, \"OAEP Reconsidered,\" Journal of Cryptology, vol. 15, no. 4, pp. 223–249, Sep. 2002 (extended abstract in Advances in Cryptology – CRYPTO 2001, LNCS 2139, pp. 239–259, Springer). https://doi.org/10.1007/s00145-002-0109-1",
        "[16] E. Fujisaki, T. Okamoto, D. Pointcheval, and J. Stern, \"RSA-OAEP is Secure under the RSA Assumption,\" Journal of Cryptology, vol. 17, no. 2, pp. 81–104, Mar. 2004 (extended abstract in Advances in Cryptology – CRYPTO 2001, LNCS 2139, pp. 260–274, Springer). https://doi.org/10.1007/s00145-002-0204-y",
        "[17] M. Bellare and P. Rogaway, \"Optimal Asymmetric Encryption,\" in Advances in Cryptology – EUROCRYPT '94, Lecture Notes in Computer Science, vol. 950, pp. 92–111, Springer, 1995. https://doi.org/10.1007/BFb0053428"
    ]

    for ref in refs:
        p_ref = add_p(space_before=0, space_after=0.1, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        p_ref.paragraph_format.left_indent = Inches(0.18)
        p_ref.paragraph_format.first_line_indent = Inches(-0.18)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = 'Times New Roman'
        r_ref.font.size = Pt(7.1)

    out_file = REPORT_DIR / "RSA_Real_World_Applications_Report.docx"
    doc.save(str(out_file))
    print(f"[+] Successfully wrote {out_file}")
    return out_file


if __name__ == "__main__":
    generate_report()
