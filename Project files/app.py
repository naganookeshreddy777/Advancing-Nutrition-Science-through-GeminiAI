import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Gemini AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.5-flash')

# Define prompt template for nutritional analysis
def create_nutrition_prompt(food_items):
    prompt = f"""
    Analyze the following food items and provide detailed nutritional information for each:
    
    Food Items: {food_items}
    
    For each food item, provide:
    1. Serving size (standard portion)
    2. Calories
    3. Macronutrients:
       - Protein (grams)
       - Fat (grams)
       - Carbohydrates (grams)
       - Fiber (grams)
    4. Key Micronutrients:
       - Important vitamins (with amounts)
       - Important minerals (with amounts)
    5. Health benefits or considerations
    
    Format the response in a clear, organized manner with each food item separated.
    """
    return prompt

# Generate AI response
def generate_nutrition_analysis(food_items):
    try:
        prompt = create_nutrition_prompt(food_items)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating analysis: {str(e)}"

# Streamlit UI
def main():
    # Page configuration
    st.set_page_config(
        page_title="Nutrition Science with Gemini AI",
        page_icon="🥗",
        layout="wide"
    )
    
    # Main title
    st.title("🥗 Advancing Nutrition Science through Gemini AI")
    st.markdown("---")
    
    # Description
    st.markdown("""
    ### Welcome to AI-Powered Nutritional Analysis
    Enter your food items below to receive comprehensive nutritional information powered by Google's Gemini AI.
    """)
    
    # User input section
    st.subheader("📝 Enter Food Items")
    food_input = st.text_area(
        "List your food items (separate with commas)",
        placeholder="e.g., apple, chicken breast, brown rice, broccoli, salmon",
        height=100
    )
    
    # Generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button("🔍 Analyze Nutrition", use_container_width=True)
    
    # Process and display results
    if analyze_button:
        if food_input.strip():
            with st.spinner("🤖 Analyzing nutritional information..."):
                # Generate analysis
                nutrition_info = generate_nutrition_analysis(food_input)
                
                # Display results
                st.markdown("---")
                st.subheader("📊 Nutritional Analysis Results")
                st.markdown(nutrition_info)
                
                # Download option
                st.download_button(
                    label="📥 Download Report",
                    data=nutrition_info,
                    file_name="nutrition_report.txt",
                    mime="text/plain"
                )
        else:
            st.warning("⚠️ Please enter at least one food item.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <small>Powered by Google Gemini AI | Nutritional information is for educational purposes</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
