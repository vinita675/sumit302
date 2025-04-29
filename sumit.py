import streamlit as st
import hashlib
import time

# Function to create a new block
def create_block(index, data, previous_hash):
    return {
        'index': index,
        'data': data,
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'previous_hash': previous_hash
    }

# Function to generate a hash for a block
def generate_hash(block):
    block_string = f"{block['index']}{block['data']}{block['timestamp']}{block['previous_hash']}"
    return hashlib.sha256(block_string.encode()).hexdigest()

# Initialize blockchain with genesis block
if 'blockchain' not in st.session_state:
    genesis_block = create_block(0, "Genesis Block", "0")
    st.session_state.blockchain = [genesis_block]

# Function to add a new ticket
def add_ticket(name, destination, seat, departure_time):
    previous_block = st.session_state.blockchain[-1]
    new_index = previous_block['index'] + 1
    new_hash = generate_hash(previous_block)

    data = {
        "name": name,
        "destination": destination,
        "seat": seat,
        "departure_time": departure_time
    }

    new_block = create_block(new_index, data, new_hash)
    st.session_state.blockchain.append(new_block)

# Streamlit UI
st.title("🚌 Bus Ticket Blockchain")

with st.form("ticket_form"):
    name = st.text_input("Passenger Name")
    destination = st.text_input("Destination")
    seat = st.text_input("Seat Number")
    departure_time = st.time_input("Departure Time")

    submitted = st.form_submit_button("Book Ticket")
    if submitted:
        if name and destination and seat:
            add_ticket(name, destination, seat, departure_time.strftime("%I:%M %p"))
            st.success("✅ Ticket added to the blockchain.")
        else:
            st.warning("Please fill in all the required fields.")

# Display Blockchain
st.subheader("📜 Ticket Blockchain")
for block in st.session_state.blockchain:
    st.markdown(f"**Block Index:** {block['index']}")
    st.json(block['data'])
    st.markdown(f"**Timestamp:** {block['timestamp']}")
    st.markdown(f"**Previous Hash:** `{block['previous_hash']}`")
    st.markdown("---")
