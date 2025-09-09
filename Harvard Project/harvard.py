import streamlit as st
import requests
import pandas as pd
import sqlite3
import json

st.title("HARVARD ARTIFACT COLLECTIONS")
st.header("📝Instructions")
st.markdown("""- In Tab 1, click Collect Data to fetch records from the Harvard Art Museums API.\n
- In Tab 2, click Import Data to save the collected artifacts into a local SQLite database and preview the tables.\n
- Use Tab 3 to select and run SQL queries to analyze artifacts by metadata, media, and colors.\n
- Explore trends, top colors, and other insights directly in the app
            """)

#Tabs
tab1, tab2, tab3 = st.tabs(["Data Collection", "Import to Database", "Analysis"])

API_KEY = "cdeded75-19a5-47d9-ae76-29ab77146e13"
names = [
    'Accessories (non-art)','Photographs','Drawings','Prints','Paintings',
    'Sculpture','Coins','Vessels','Textile Arts','Archival Material',
    'Fragments','Manuscripts','Seals','Straus Materials'
]

# Tab 1 
with tab1:
    st.header("🏺Artifact Classifications")
    select = st.selectbox("Choose an option", names)

    if st.button("Collect Data"):
        data2 = []
        for i in range(1, 26):
            url = "https://api.harvardartmuseums.org/object"
            params = {
                "apikey": API_KEY,
                "size": 100,
                "page": i,
                "classification": select
            }
            response = requests.get(url, params)
            data = response.json()
            data2.extend(data['records'])

        # Split into metadata, media, colors
        metadata, artifact_media, artifact_colors = [], [], []
        for i in data2:
            metadata.append(dict(
                objid=i['objectid'],
                id=i['id'],
                title=i.get('title'),
                culture=i.get('culture'),
                period=i.get('period'),
                century=i.get('century'),
                medium=i.get('medium'),
                dimensions=i.get('dimensions'),
                description=i.get('description'),
                department=i.get('department'),
                classification=i.get('classification'),
                accessionyear=i.get('accessionyear'),
                accessionmethod=i.get('accessionmethod'),
            ))
            artifact_media.append(dict(
                objid=i['objectid'],
                imagecount=i.get('imagecount'),
                mediacount=i.get('mediacount'),
                colorcount=i.get('colorcount'),
                rank=i.get('rank'),
                datebegin=i.get('datebegin'),
                dateend=i.get('dateend')
            ))
            if i.get('colors'):
                for c in i['colors']:
                    artifact_colors.append(dict(
                        objid=i['objectid'],
                        color=c.get('color'),
                        spectrum=c.get('spectrum'),
                        hue=c.get('hue'),
                        percent=c.get('percent'),
                        css3=c.get('css3')
                    ))

        # Save to session state
        st.session_state.metadata = metadata
        st.session_state.artifact_media = artifact_media
        st.session_state.artifact_colors = artifact_colors

        st.subheader("Metadata JSON")
        st.json(metadata[:3]) 

        st.subheader("Artifact Media JSON")
        st.json(artifact_media[:3])

        st.subheader("Artifact Colors JSON")
        st.json(artifact_colors[:3])


# Tab 2
with tab2:
    st.header("🗄️Import Collected Data")

    if st.button("Import Data"):
        metadata_df = pd.DataFrame(st.session_state.get("metadata", []))
        media_df = pd.DataFrame(st.session_state.get("artifact_media", []))
        colors_df = pd.DataFrame(st.session_state.get("artifact_colors", []))

        #Import to database
        conn = sqlite3.connect(r"D:\Harvard Project\artifact_details.db")
        if not metadata_df.empty:
            metadata_df.to_sql("metadata", conn, if_exists="replace", index=False)
        if not media_df.empty:
            media_df.to_sql("artifact_media", conn, if_exists="replace", index=False)
        if not colors_df.empty:
            colors_df.to_sql("artifact_colors", conn, if_exists="replace", index=False)
        conn.close()

        st.success("✅ Data imported successfully!")

        # Tabs for preview
        tab4, tab5, tab6 = st.tabs(["Metadata", "Artifact Media", "Artifact Colors"])
        with tab4:
            st.dataframe(metadata_df.head(10))
        with tab5:
            st.dataframe(media_df.head(10))
        with tab6:
            st.dataframe(colors_df.head(10))

with tab3:
    st.header("🔎Query & Analysis")

    queries = {
        "List all artifacts from the 11th century belonging to Byzantine culture.": 
            "SELECT * FROM metadata WHERE culture='Byzantine' AND century='11th century';",

        "What are the unique cultures represented in the artifacts?": 
            "SELECT DISTINCT culture FROM metadata;",

        "List all artifacts from the Archaic Period.": 
            "SELECT * FROM metadata WHERE period='Archaic';",

        "List artifact titles ordered by accession year in descending order.": 
            "SELECT title, accessionyear FROM metadata ORDER BY accessionyear DESC;",

        "How many artifacts are there per department?": 
            "SELECT department, COUNT(*) as artifact_count FROM metadata GROUP BY department;",

        "Which artifacts have more than 1 image?": 
            "SELECT objid, imagecount FROM artifact_media WHERE imagecount > 1;",

        "What is the average rank of all artifacts?": 
            "SELECT AVG(rank) as avg_rank FROM artifact_media;",

        "Which artifacts have a higher colorcount than mediacount?": 
            "SELECT objid, colorcount, mediacount FROM artifact_media WHERE colorcount > mediacount;",

        "List all artifacts created between 1500 and 1600.": 
            "SELECT * FROM artifact_media WHERE datebegin >= 1500 AND dateend <= 1600;",

        "How many artifacts have no media files?": 
            "SELECT COUNT(*) as no_media_count FROM artifact_media WHERE mediacount=0;",

        "What are all the distinct hues used in the dataset?": 
            "SELECT DISTINCT hue FROM artifact_colors;",

        "What are the top 5 most used colors by frequency?": 
            "SELECT color, COUNT(*) as frequency FROM artifact_colors GROUP BY color ORDER BY frequency DESC LIMIT 5;",

        "What is the average coverage percentage for each hue?": 
            "SELECT hue, AVG(percent) as avg_coverage FROM artifact_colors GROUP BY hue;",

        "What is the total number of color entries in the dataset?": 
            "SELECT COUNT(*) as total_colors FROM artifact_colors;",

        "List artifact titles and hues for all artifacts belonging to the Byzantine culture.": 
            "SELECT m.title, c.hue FROM metadata m JOIN artifact_colors c ON m.objid = c.objid WHERE m.culture='Byzantine';",

        "List each artifact title with its associated hues.": 
            "SELECT m.title, c.hue FROM metadata m JOIN artifact_colors c ON m.objid = c.objid;",

        "Get artifact titles, cultures, and media ranks where the period is not null.": 
            "SELECT m.title, m.culture, am.rank FROM metadata m JOIN artifact_media am ON m.objid = am.objid WHERE m.period IS NOT NULL;",

        "Find artifact titles ranked in the top 10 that include the color hue 'Grey'.": 
            "SELECT m.title, am.rank FROM metadata m JOIN artifact_media am ON m.objid = am.objid JOIN artifact_colors c ON m.objid = c.objid WHERE c.hue='Grey' ORDER BY a.rank ASC LIMIT 10;",

        "How many artifacts exist per classification, and what is the average media count for each?": 
            "SELECT m.classification, COUNT(*) as artifact_count, AVG(am.mediacount) as avg_media_count FROM metadata m JOIN artifact_media am ON m.objid = am.objid GROUP BY m.classification;"
    }

    selected_query = st.selectbox("Select a Query to Analyse", list(queries.keys()))

    if st.button("Analyse"):
        connect = sqlite3.connect(r"D:\Harvard Project\artifact_details.db")
        
        sql = queries[selected_query]   
        df = pd.read_sql(sql, connect)   
        
        st.dataframe(df) 
        
        connect.close()
