import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import ndjson


st.title('Google Quickdraw Analysis')


def transform_drawing(drawing):
    return {'key_id': drawing['key_id'], 'strokes': [{'x': draw[0], 'y': draw[1]} for draw in drawing['drawing']]}


@st.cache
def load_data(drawing_count):
    # load from file-like objects
    with open('house.ndjson') as f:
        drawings = ndjson.load(f)
        return [transform_drawing(drawing) for drawing in drawings[0:drawing_count] if len(drawing['drawing']) > 5]


num_drawings = st.slider('Drawings', 100, 10000, 100)
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
raw_drawings = load_data(num_drawings)
data_load_state.text('✓ Data loaded!')

# Notify the reader that the data was successfully loaded.
st.write('Do people draw outside-in or inside-out?')
st.write('Questions like this are interesting case studies in neural diversity!')
st.write('By Arsala Bangash')


@st.cache
def convert_data_to_dataframe(raw_data):
    return pd.DataFrame.from_dict(raw_data)


if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(convert_data_to_dataframe(raw_drawings))

st.write("-----------------------------------------------------------------------------")
st.write("Studies have found that children with ASD tend to draw 'fragmented' pictures (disjointed appearance in the drawing) when compared to TD children. (Fein et al. 1990) (Booth et al. 2003)")
st.write("This could be linked with the total number of strokes used (ex. drawing a window by drawing two intersecting lines versus drawing four separate lines)")
st.write('Looking at the distribution of strokes used to complete the drawing:')
total_strokes = (np.array([len(drawing['strokes'])
                           for drawing in raw_drawings]))
plt.hist(x=total_strokes, bins=num_drawings//5, color='blue',
         edgecolor='black', alpha=0.7, rwidth=0.85, histtype='stepfilled')
plt.title('Histogram of Strokes Used')
plt.xlabel('Number of Strokes')
plt.ylabel('Frequency')

plt.show()
st.pyplot()

st.write("Potential follow-up questions:")
st.write("1) For people who use more strokes than the average, are they drawing in a similar pattern (ie. inside-out vs outside-in)?")
st.write("2) Is there anything similar about their location (ex. people in close locations have different interpretation of the same word and require more strokes)? ")


st.write("-----------------------------------------------------------------------------------------------")

st.header('Plots')
st.write("Plotting each drawing's strokes show us how they evolve over time.")
st.write('Here we can differentiate between drawings that were drawing inside-out or outside-in.')

for drawing in raw_drawings:
    plt.gca().invert_yaxis()
    st.subheader("ID: {}".format(drawing['key_id']))
    for stroke_number, stroke in enumerate(drawing['strokes']):
        plt.plot(stroke['x'], stroke['y'],
                 label='Stroke {}'.format(stroke_number))
        plt.legend(loc='upper center', bbox_to_anchor=(0.7, 1.15),
                   ncol=3, fancybox=True, shadow=True)
    st.pyplot()
    plt.clf()
