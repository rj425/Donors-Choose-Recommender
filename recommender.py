import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from PIL import Image
from scripts.query_reco_engine import query_reco_engine

# Setting the title
st.title("DonorsChoose Recommender! :sunglasses:")
with st.spinner('Loading recommendation engine...'):
    try:
        from scripts.data_ingestion import donors, categories, us_cities, reco_engine
    except Exception as e:
        st.info("Please make sure all the required dataset files and 'reco_engine.csv' are present in 'data' directory")
        st.error("Something went wrong! :confused:")
        raise(e)


def construct_sidebar():
    with st.spinner("Constructing Sidebar..."):
        st.sidebar.title("Project Profile")
        input_fields = {}
        for column in categories.columns:
            input_fields[column] = st.sidebar.selectbox(
                column, categories[column].unique())
        # Adding state multiseect and Submit button
        user_state = st.sidebar.multiselect(
            "Preferred State (Optional)", us_cities["state_name"].dropna().unique())
        clicked = st.sidebar.button("Submit")
    return input_fields, user_state, clicked


def recommend_donors(input_fields, top_k, user_state):
    with st.spinner("Recommending Donors..."):
        st.subheader("Recommended Donors")
        recommended_donor_ids = query_reco_engine(
            input_fields,
            reco_engine,
            categories.columns,
            top_k,
            categories
        )
        recommended_donors = donors[donors["Donor ID"].isin(
            recommended_donor_ids)]
        recommended_donors = recommended_donors.merge(us_cities, left_on=["Donor City", "Donor State"], right_on=[
            "city", "state_name"], how="inner")
        columns = [
            "Donor City",
            "Donor State",
            "Donor Is Teacher",
            "Donor Zip",
            "lat",
            "lon"
        ]
        recommended_donors = recommended_donors[columns]
        if len(user_state) > 0:
            recommended_donors = recommended_donors[recommended_donors["Donor State"].isin(
                user_state)]
    return recommended_donors


def load_map(recommended_donors):
    with st.spinner("Loading donor's map..."):
        st.subheader("Recommended Donors' Location")
        layer1 = pdk.Layer(
            "ScatterplotLayer",
            recommended_donors,
            auto_highlight=True,
            opacity=1,
            get_position=["lon", "lat"],
            get_radius=50000,
            get_fill_color=[0, 0, 200, 140],
            pickable=True
        )
        midpoint = (np.average(recommended_donors["lat"]), np.average(
            recommended_donors["lon"]))
        view_state = pdk.ViewState(
            longitude=midpoint[1],
            latitude=midpoint[0],
            zoom=3,
            min_zoom=1,
            max_zoom=15,
        )
        donors_map = pdk.Deck(layers=[layer1], initial_view_state=view_state,
                              map_style="", tooltip=True)
        st.write(donors_map)


def plot_charts(recommended_donors):
    with st.spinner("Plotting charts..."):
        df1 = recommended_donors.groupby(['Donor State']).size().to_frame(
            name='Donor Count').sort_values(by='Donor Count', ascending=False)
        st.subheader("Statewise Donors' count")
        st.bar_chart(df1)
        df2 = recommended_donors.groupby(['Donor City', 'Donor State']).size().to_frame(
            'Donor Count').sort_values(by='Donor Count', ascending=False).reset_index()
        st.subheader("Citywise Donors' Count")
        st.write(df2)


if __name__ == "__main__":
    # Constructing sidebar
    input_fields, user_state, clicked = construct_sidebar()
    # On button click
    if clicked:
        # Recommending Donors
        top_k = 200
        recommended_donors = recommend_donors(
            input_fields, top_k, user_state)
        st.write(recommended_donors)
        # Loading donors map
        load_map(recommended_donors)
        # Plotting donors" stats
        plot_charts(recommended_donors)
    else:
        # Loading a cover image
        image = Image.open("images/cover.png")
        st.image(image, caption="Support a classroom. Build a future",
                    use_column_width=True)
