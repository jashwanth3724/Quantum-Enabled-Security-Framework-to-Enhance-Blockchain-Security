import streamlit as st
import time
import random
import hashlib
import secrets

from rsa_module import generate_rsa_keys
from shor_attack import shor_factor

st.set_page_config(page_title="Quantum Blockchain Live Demo", layout="wide")

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
defaults = {
    "chain": [],
    "rsa_keys": [],
    "target_block": None,
    "attack_complete": False,
    "pqc_enabled": False,
    "console_log": [],
    "current_mode": "Classical RSA",
    "pqc_details": {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

participants = ["Likhitha", "Jashwanth", "Poorvi", "Abishek", "Santhosh"]

# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------
def current_stage():
    if st.session_state.pqc_enabled:
        return "pqc"
    if st.session_state.attack_complete:
        return "compromised"
    if st.session_state.target_block is not None:
        return "attack"
    return "secure"

def log_event(msg):
    st.session_state.console_log.append(msg)

def short_hash(h):
    if not h:
        return "0"
    return h[:16] + "..." + h[-10:] if len(h) > 30 else h

def tx_summary(transaction_text):
    parts = transaction_text.split()
    if len(parts) >= 6 and parts[1] == "sends":
        return parts[0], parts[2], parts[-1]
    return "System", "-", "-"

def get_status():
    if st.session_state.pqc_enabled:
        return "PQC Protected"
    if st.session_state.attack_complete:
        return "Compromised"
    if st.session_state.target_block is not None:
        return "Under Attack"
    return "Secure"

# ---------------------------------------------------
# DATA MODEL
# ---------------------------------------------------
class Block:
    def __init__(self, index, transaction, previous_hash):
        self.index = index
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        raw = f"{self.index}{self.transaction}{self.previous_hash}"
        return hashlib.sha256(raw.encode()).hexdigest()

# ---------------------------------------------------
# STYLE
# ---------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(0,198,255,0.14), transparent 28%),
        radial-gradient(circle at top right, rgba(122,92,255,0.12), transparent 30%),
        linear-gradient(135deg, #03101c 0%, #081b2d 45%, #09253a 100%);
    color: #eaf6ff;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.main-title {
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 34px;
    font-weight: 800;
    color: white;
    margin-top: 8px;
    margin-bottom: 4px;
    text-shadow: 0 0 16px rgba(0,198,255,0.35);
}

.sub-title {
    text-align: center;
    color: #9fdcff;
    font-size: 15px;
    margin-bottom: 10px;
}

.glow-line {
    height: 4px;
    border-radius: 999px;
    background: linear-gradient(90deg, #00c6ff, #7a5cff, #00ffa3, #00c6ff);
    background-size: 300% 100%;
    animation: glowbar 6s linear infinite;
    margin-bottom: 18px;
}

@keyframes glowbar {
    0% {background-position: 0% 50%;}
    100% {background-position: 300% 50%;}
}

.section-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 18px;
    margin-bottom: 18px;
    backdrop-filter: blur(12px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.22);
}

.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 16px;
    text-align: center;
}

.metric-label {
    color: #91d8ff;
    font-size: 13px;
    margin-bottom: 6px;
    text-transform: uppercase;
}

.metric-value {
    color: white;
    font-size: 22px;
    font-weight: 800;
}

.chip-row {
    text-align: center;
    margin-bottom: 15px;
}

.chip {
    display: inline-block;
    padding: 10px 16px;
    margin: 4px 6px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    opacity: 0.45;
}

.chip.active {
    opacity: 1;
    transform: scale(1.05);
}

.secure-chip { color: #9cffc7; border: 1px solid rgba(46,204,113,0.45); background: rgba(46,204,113,0.10); }
.attack-chip { color: #ffe38a; border: 1px solid rgba(241,181,28,0.45); background: rgba(241,181,28,0.10); }
.comp-chip { color: #ffaaa2; border: 1px solid rgba(231,76,60,0.45); background: rgba(231,76,60,0.10); }
.pqc-chip { color: #9fd6ff; border: 1px solid rgba(58,160,255,0.45); background: rgba(58,160,255,0.10); }

.secure-chip.active { box-shadow: 0 0 16px rgba(46,204,113,0.35); }
.attack-chip.active { box-shadow: 0 0 16px rgba(241,181,28,0.35); }
.comp-chip.active { box-shadow: 0 0 16px rgba(231,76,60,0.35); }
.pqc-chip.active { box-shadow: 0 0 16px rgba(58,160,255,0.35); }

.console-box {
    background: linear-gradient(180deg, #071018 0%, #08141d 100%);
    color: #9effd7;
    border-radius: 16px;
    padding: 14px;
    border: 1px solid #19354a;
    font-family: Consolas, monospace;
    font-size: 14px;
    min-height: 180px;
    white-space: pre-wrap;
}

.live-panel {
    background: linear-gradient(180deg, rgba(0,198,255,0.08), rgba(122,92,255,0.08));
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 12px;
    margin-top: 12px;
    min-height: 280px;
}

.live-banner {
    padding: 12px 16px;
    border-radius: 16px;
    background: rgba(0,198,255,0.08);
    border: 1px solid rgba(0,198,255,0.18);
    color: #c9f2ff;
    font-weight: 700;
    text-align: center;
    margin-bottom: 14px;
}

.stButton > button {
    width: 100%;
    border: none;
    border-radius: 14px;
    padding: 0.80rem 1rem;
    font-weight: 800;
    color: white;
    background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
header_placeholder = st.empty()
metrics_placeholder = st.empty()

def render_header():
    with header_placeholder.container():
        st.markdown('<div class="main-title">⚛ QUANTUM-ENABLED BLOCKCHAIN SECURITY DASHBOARD</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sub-title">Live demonstration of Shor attack, blockchain compromise, and post-quantum protection using QRNG, QKD, and Dilithium-style security</div>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)

        stage = current_stage()
        secure_cls = "chip secure-chip active" if stage == "secure" else "chip secure-chip"
        attack_cls = "chip attack-chip active" if stage == "attack" else "chip attack-chip"
        comp_cls = "chip comp-chip active" if stage == "compromised" else "chip comp-chip"
        pqc_cls = "chip pqc-chip active" if stage == "pqc" else "chip pqc-chip"

        st.markdown(f"""
        <div class="chip-row">
            <span class="{secure_cls}">SECURE</span>
            <span class="{attack_cls}">UNDER ATTACK</span>
            <span class="{comp_cls}">COMPROMISED</span>
            <span class="{pqc_cls}">PQC PROTECTED</span>
        </div>
        """, unsafe_allow_html=True)

def render_metrics():
    with metrics_placeholder.container():
        status = get_status()
        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Mode</div><div class="metric-value">{st.session_state.current_mode}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Status</div><div class="metric-value">{status}</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Blocks</div><div class="metric-value">{len(st.session_state.chain)}</div></div>', unsafe_allow_html=True)
        with m4:
            target = "-" if st.session_state.target_block is None else str(st.session_state.target_block)
            st.markdown(f'<div class="metric-card"><div class="metric-label">Target</div><div class="metric-value">{target}</div></div>', unsafe_allow_html=True)

render_header()
render_metrics()

# ---------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------
left, right = st.columns([2.1, 1.1])

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("⛓ Live Blockchain")
    blockchain_placeholder = st.empty()
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="live-banner">⚡ Real-time quantum attack and defense simulation</div>', unsafe_allow_html=True)

    st.subheader("🎛 Controls")
    b1, b2 = st.columns(2)
    with b1:
        build_clicked = st.button("Build Blockchain")
    with b2:
        shor_clicked = st.button("Run Shor Attack")

    b3, b4 = st.columns(2)
    with b3:
        manipulate_clicked = st.button("Manipulate Block")
    with b4:
        pqc_clicked = st.button("Enable PQC")

    reset_clicked = st.button("Reset Demo")

    st.subheader("🖥 Live Console")
    console_placeholder = st.empty()

    st.subheader("⚡ Live Action Panel")
    live_placeholder = st.empty()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# RENDERERS
# ---------------------------------------------------
def render_console():
    text = "\n".join(st.session_state.console_log[-12:]) if st.session_state.console_log else "No live events yet."
    console_placeholder.markdown(f'<div class="console-box">{text}</div>', unsafe_allow_html=True)

def render_live_panel_default():
    with live_placeholder.container():
        st.markdown('<div class="live-panel">Action output will appear here. No scrolling needed.</div>', unsafe_allow_html=True)

def render_block_streamlit(block, mode):
    sender, amount, receiver = tx_summary(block.transaction)

    if mode == "target":
        title = f"🎯 Target Block #{block.index}"
        box_func = st.warning
        tag = "Shor Target"
    elif mode == "compromised":
        title = f"⚠ Compromised Block #{block.index}"
        box_func = st.error
        tag = "Integrity Broken"
    elif mode == "pqc":
        title = f"🛡 Protected Block #{block.index}"
        box_func = st.info
        tag = "PQC Enabled"
    else:
        title = f"✅ Active Block #{block.index}"
        box_func = st.success
        tag = "Classical RSA"

    with st.container(border=True):
        box_func(title)
        st.caption(tag)
        st.markdown("**Transaction Flow**")
        st.write(f"{sender} → {receiver}")
        st.write(f"**Amount:** {amount} BTC")
        st.write(f"**Hash:** `{short_hash(block.hash)}`")
        st.write(f"**Previous Hash:** `{short_hash(block.previous_hash)}`")

def render_chain():
    with blockchain_placeholder.container():
        if not st.session_state.chain:
            st.info("Build the blockchain to begin.")
            return

        st.markdown("**Legend:** ✅ Normal | 🎯 Targeted by Shor | ⚠ Compromised | 🛡 PQC Protected")
        total = len(st.session_state.chain)
        cols_per_row = 3

        for row_start in range(0, total, cols_per_row):
            row_blocks = st.session_state.chain[row_start:row_start + cols_per_row]
            cols = st.columns(len(row_blocks))

            for idx, block in enumerate(row_blocks):
                i = row_start + idx
                with cols[idx]:
                    mode = "normal"
                    if st.session_state.pqc_enabled:
                        mode = "pqc"
                    elif i == st.session_state.target_block and not st.session_state.attack_complete:
                        mode = "target"
                    elif i == st.session_state.target_block and st.session_state.attack_complete:
                        mode = "compromised"

                    render_block_streamlit(block, mode)

render_console()
render_live_panel_default()
render_chain()

# ---------------------------------------------------
# ACTIONS
# ---------------------------------------------------
if reset_clicked:
    st.session_state.chain = []
    st.session_state.rsa_keys = []
    st.session_state.target_block = None
    st.session_state.attack_complete = False
    st.session_state.pqc_enabled = False
    st.session_state.console_log = []
    st.session_state.current_mode = "Classical RSA"
    st.session_state.pqc_details = {}
    render_header()
    render_metrics()
    render_console()
    render_live_panel_default()
    render_chain()

if build_clicked:
    st.session_state.chain = []
    st.session_state.rsa_keys = []
    st.session_state.target_block = None
    st.session_state.attack_complete = False
    st.session_state.pqc_enabled = False
    st.session_state.console_log = []
    st.session_state.current_mode = "Classical RSA"
    st.session_state.pqc_details = {}

    render_header()
    render_metrics()
    render_console()
    render_chain()

    with live_placeholder.container():
        st.markdown('<div class="live-panel">', unsafe_allow_html=True)
        st.subheader("🏗 Live Blockchain Build")
        status_box = st.empty()
        progress = st.progress(0)

        genesis = Block(0, "Genesis Block", "0")
        st.session_state.chain.append(genesis)
        pub, priv, p, q = generate_rsa_keys()
        st.session_state.rsa_keys.append((pub, priv))
        log_event("[Build] Genesis block created.")

        status_box.success("Genesis block added to blockchain.")
        render_console()
        render_chain()
        render_metrics()
        time.sleep(1.2)

        total_blocks = random.randint(4, 7)
        for i in range(1, total_blocks):
            sender = random.choice(participants)
            receiver = random.choice(participants)
            while receiver == sender:
                receiver = random.choice(participants)

            amount = random.randint(100, 1000)
            tx = f"{sender} sends {amount} BTC to {receiver}"

            status_box.info(f"Mining Block {i}...")
            time.sleep(0.8)

            block = Block(i, tx, st.session_state.chain[-1].hash)
            st.session_state.chain.append(block)
            pub, priv, p, q = generate_rsa_keys()
            st.session_state.rsa_keys.append((pub, priv))

            log_event(f"[Build] Block {i} mined: {tx}")
            progress.progress(int(((i + 1) / total_blocks) * 100))

            render_console()
            render_chain()
            render_metrics()

            status_box.success(f"Block {i} added successfully.")
            time.sleep(1.4)

        st.success("Blockchain build completed.")
        st.markdown('</div>', unsafe_allow_html=True)

if shor_clicked and st.session_state.chain and not st.session_state.pqc_enabled:
    st.session_state.target_block = random.randint(1, len(st.session_state.chain) - 1)
    render_header()
    render_metrics()
    render_chain()

    log_event(f"[Attack] Target selected: Block {st.session_state.target_block}")
    render_console()

    with live_placeholder.container():
        st.markdown('<div class="live-panel">', unsafe_allow_html=True)
        st.subheader("⚡ Live Shor Attack")
        progress = st.progress(0)
        step_box = st.empty()

        steps = [
            "Initializing quantum registers",
            "Preparing superposition",
            "Applying modular exponentiation",
            "Running Quantum Fourier Transform",
            "Finding hidden period",
            "Deriving RSA factors"
        ]

        for i, step in enumerate(steps):
            step_box.info(step)
            log_event(f"[Shor] {step}")
            render_console()
            progress.progress(int((i + 1) * 100 / len(steps)))
            time.sleep(0.9)

        pub = st.session_state.rsa_keys[st.session_state.target_block][0]
        e, N = pub
        st.write(f"Factoring RSA modulus: **{N}**")
        p, q = shor_factor(N)
        st.error(f"Factors Found: {p}, {q}")
        phi = (p - 1) * (q - 1)
        d = pow(e, -1, phi)
        st.success(f"Private Key Recovered: {d}")

        log_event(f"[Attack] Private key recovered for Block {st.session_state.target_block}.")
        st.session_state.attack_complete = True

        render_header()
        render_metrics()
        render_console()
        render_chain()
        st.markdown('</div>', unsafe_allow_html=True)

if manipulate_clicked and st.session_state.attack_complete and not st.session_state.pqc_enabled:
    target = st.session_state.target_block
    sender = random.choice(participants)
    receiver = random.choice(participants)
    while receiver == sender:
        receiver = random.choice(participants)

    amount = random.randint(500, 2000)
    new_tx = f"{sender} sends {amount} BTC to {receiver}"
    prev_hash = st.session_state.chain[target - 1].hash
    st.session_state.chain[target] = Block(target, new_tx, prev_hash)

    log_event(f"[Exploit] Block {target} tampered: {new_tx}")
    render_console()
    render_chain()
    render_metrics()
    render_header()

    with live_placeholder.container():
        st.markdown('<div class="live-panel">', unsafe_allow_html=True)
        st.subheader("💥 Live Blockchain Manipulation")
        st.error(f"Block {target} has been tampered.")
        st.write(f"Forged transaction: **{new_tx}**")
        time.sleep(1.2)
        st.markdown('</div>', unsafe_allow_html=True)

if pqc_clicked and st.session_state.chain:
    st.session_state.pqc_enabled = True
    st.session_state.attack_complete = False
    st.session_state.current_mode = "PQC Protected"

    render_header()
    render_metrics()
    render_chain()

    with live_placeholder.container():
        st.markdown('<div class="live-panel">', unsafe_allow_html=True)
        st.subheader("🛡 Live PQC Activation")

        st.info("QRNG: Initializing quantum entropy source...")
        time.sleep(0.8)
        qrng_seed = secrets.randbits(256)
        st.code(str(qrng_seed))
        log_event("[QRNG] Quantum-safe random seed generated.")
        render_console()

        st.info("QKD: Establishing quantum communication channel...")
        time.sleep(0.8)
        st.info("QKD: Matching measurement bases...")
        time.sleep(0.8)
        shared_key = hashlib.sha256(str(secrets.randbits(256)).encode()).hexdigest()
        st.code(shared_key)
        log_event("[QKD] Shared secret key established.")
        render_console()

        st.info("Dilithium: Generating post-quantum signature...")
        time.sleep(0.8)
        private_key = secrets.randbits(256)
        public_key = private_key * 2
        signature = hashlib.sha256(("Blockchain Transaction" + str(private_key)).encode()).hexdigest()
        st.code(str(public_key))
        st.code(signature)
        log_event("[Dilithium] Post-quantum signature attached to blockchain.")
        render_console()

        st.session_state.pqc_details = {
            "qrng_seed": qrng_seed,
            "shared_key": shared_key,
            "public_key": public_key,
            "signature": signature,
        }

        log_event("[Defense] Blockchain switched to PQC mode.")
        render_console()
        render_header()
        render_metrics()
        render_chain()

        st.success("Post-quantum protection is now active.")
        st.markdown('</div>', unsafe_allow_html=True)

if shor_clicked and st.session_state.chain and st.session_state.pqc_enabled:
    st.session_state.target_block = random.randint(1, len(st.session_state.chain) - 1)
    render_header()
    render_metrics()
    render_chain()

    log_event(f"[Attack] Target selected after PQC: Block {st.session_state.target_block}")
    render_console()

    with live_placeholder.container():
        st.markdown('<div class="live-panel">', unsafe_allow_html=True)
        st.subheader("⚡ Live Shor Attack on PQC-Protected Blockchain")
        progress = st.progress(0)
        step_box = st.empty()

        steps = [
            "Initializing quantum registers",
            "Preparing superposition",
            "Applying modular exponentiation",
            "Running Quantum Fourier Transform",
            "Attempting signature break"
        ]

        for i, step in enumerate(steps):
            step_box.info(step)
            log_event(f"[Shor] {step}")
            render_console()
            progress.progress(int((i + 1) * 100 / len(steps)))
            time.sleep(0.9)

        st.error("Factorization Failed")
        st.success("Shor attack failed against PQC protection.")
        log_event("[Defense] PQC protection resisted the Shor attack.")
        render_console()
        render_header()
        render_metrics()
        render_chain()
        st.markdown('</div>', unsafe_allow_html=True)