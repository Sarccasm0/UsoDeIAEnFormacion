import streamlit as st
import pandas as pd
import math
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title
st.title("CSV Data Visualization")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    try:
        df = pd.read_csv(uploaded_file)
        
        # Display the dataframe
        st.subheader("Data Preview")
        st.dataframe(df.head())
        
        # Get basic statistics
        st.subheader("Basic Statistics")
        st.write(df.describe())
        
        # Select columns for visualization
        st.subheader("Create Visualization")
        
        # Check if the dataframe has numeric columns
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        if len(numeric_columns) > 0:
            # Column selection
            x_axis = st.selectbox("Select X-axis", df.columns)
            y_axis = st.selectbox("Select Y-axis", numeric_columns)
            
            # Chart type selection
            chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot"])
            
            # Create the plot
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if chart_type == "Bar Chart":
                sns.barplot(x=x_axis, y=y_axis, data=df, ax=ax)
            elif chart_type == "Line Chart":
                sns.lineplot(x=x_axis, y=y_axis, data=df, ax=ax)
            else:  # Scatter Plot
                sns.scatterplot(x=x_axis, y=y_axis, data=df, ax=ax)
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Display the plot
            st.pyplot(fig)
            
            # Option to download the plot
            st.subheader("Download Options")
            if st.button("Download Plot as PNG"):
                # Save the figure
                plt.savefig("plot.png", dpi=300, bbox_inches="tight")
                st.success("Plot saved as 'plot.png'")
        else:
            st.warning("No numeric columns found in the dataset for visualization.")
    
    except Exception as e:
        st.error(f"Error reading the file: {e}")
else:
    st.info("Please upload a CSV file to continue.")