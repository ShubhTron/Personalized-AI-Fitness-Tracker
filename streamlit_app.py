import streamlit as st
import pandas as pd
import joblib
import streamlit.components.v1 as components
import streamlit as st
import requests

# Replace with Render backend URL
BACKEND_URL = "https://your-backend-service.onrender.com"

st.title("My Streamlit App")

response = requests.get(f"{BACKEND_URL}/api/data")
if response.status_code == 200:
    data = response.json()
    st.write("Data from backend:", data)
else:
    st.error("Failed to fetch data")
# Function for loading model
@st.cache_data
def load_model():
    with open('miniproject/calories_model', 'rb') as file:
        loaded_model = joblib.load(file)
    return loaded_model

# Load your model
loaded_model = load_model()

# Sidebar for navigation
st.sidebar.title('Welcome, user 🏃‍♂️...')
options = st.sidebar.selectbox('📁Browse', ['🔗 Predicto-meter', '🔗 Description'])

# Set custom CSS for the light theme
st.markdown("""
    <style>
    body {
        background-color: #ffffff; /* White background */
        color: #000080; /* Navy text color */
    }

    .stSidebar {
        background-color: #dbe8f8; /* Soft blue sidebar */
    }

    h1, h2, h3, h4, h5, h6 {
        color: #000080; /* Dark blue for all headings */
    }

    .stButton>button {
        background-color: #0066cc; /* Blue button */
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #004a99; /* Darker blue on hover */
        transform: scale(1.05); /* Slight grow effect */
    }

    .st-expander .st-expander-content {
        background-color: #e7f3ff; /* Light blue for expanders */
    }

    .info-container {
        background-color: #e7f3ff; /* Light blue container */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        font-family: 'Arial', sans-serif;
    }

    .info-container:hover {
        transform: scale(1.02); 
        box-shadow: 0 0 15px rgba(0, 102, 204, 0.4); /* Blue glow */
    }

    .custom-container, .desc-container {
        background-color: #e7f3ff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }

    .custom-container:hover, .desc-container:hover {
        box-shadow: 0 0 15px rgba(0, 102, 204, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

if options == '🔗 Predicto-meter':  # Prediction page
    st.title('🕰️ You have been working hard, it’s time for the results...')

    # User inputs
    gender = st.selectbox('Gender', ['Male', 'Female'])
    age = st.number_input('Age', 1, 100, 25)
    height = st.number_input('Height in cm', 100, 250, 170)
    weight = st.number_input('Weight in kg', 30, 200, 70)
    duration = st.number_input('Duration in minutes', 1, 180, 60)
    heart_rate = st.number_input('Heart Rate', 60, 200, 100)
    body_temp = st.number_input('Body Temperature in Celsius', 35.0, 43.0, 37.0)

    user_inputs = {
        'gender': 0 if gender == 'Male' else 1,
        'age': age,
        'height': height,
        'weight': weight,
        'duration': duration,
        'heart_rate': heart_rate,
        'body_temp': body_temp
    }

    if st.button('CALCULATE 🧠'):
        prediction = loaded_model.predict(pd.DataFrame(user_inputs, index=[0]))
        st.markdown(f'### YAY!!..You burned : {prediction[0]:,.2f} calories. Keep going 🏅')

        with st.expander("Show more details"):
            st.write("Details of the prediction:")
            st.write('Model used: Xtreme Gradient Boost Regressor')

elif options == '🔗 Description':
    st.markdown("<h1 style='font-size: 40px;'>📌 Factors Influencing Calorie Burn</h1>", unsafe_allow_html=True)

    st.markdown("""
        <div class="info-container">
            <h3 style="text-align: center;">Decisive Factors</h3>
            <ul>
                <li><b>Age:</b> As we age, our metabolism naturally slows down.</li>
                <li><b>Weight:</b> Heavier individuals burn more calories.</li>
                <li><b>Gender:</b> Muscle mass and hormones impact calorie burn.</li>
                <li><b>Height:</b> Taller individuals have higher metabolic rates.</li>
                <li><b>Duration:</b> Longer exercise means more calories burned.</li>
                <li><b>Heart Rate:</b> Higher intensity leads to higher calorie burn.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Carousel
    st.markdown("<h2 style='text-align: center;'>Transform your lifestyle !!!....</h2>", unsafe_allow_html=True)

    carousel_html = """
    <div class="swiper">
        <div class="swiper-wrapper">
            <div class="swiper-slide"><img src="https://i.pinimg.com/originals/05/42/e0/0542e0807d4b0884378c15051a0c61d7.jpg"></div>
            <div class="swiper-slide"><img src="https://i0.wp.com/thedifferenceapp.com/wp-content/uploads/2023/01/Infographic-for-Activity-Burn-at-Different-Paces.png?resize=768%2C431&ssl=1"></div>
            <div class="swiper-slide"><img src="https://www.verywellfit.com/thmb/N3wnFUCZqddd6NFJjkkANMVBUP0=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/how-many-calories-do-i-burn-every-day-3495464-final-dc03506ae07344f5a7ebeb4d3da0d90d.jpg"></div>
        </div>
        <div class="swiper-pagination"></div>
        <div class="swiper-button-prev"></div>
        <div class="swiper-button-next"></div>
    </div>

    <script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>

    <script>
      const swiper = new Swiper('.swiper', {
          loop: true,
          spaceBetween: 30,
          slidesPerView: 1,
          centeredSlides: true,
          pagination: {
              el: '.swiper-pagination',
              clickable: true,
          },
          navigation: {
              nextEl: '.swiper-button-next',
              prevEl: '.swiper-button-prev',
          },
      });
    </script>
    """

    components.html(carousel_html, height=500)