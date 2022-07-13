import folium

def create_map(coord1,city1,coord2,city2,coord3,city3):

    m=folium.Map(location=[46.71109, 1.7191036],zoom_start=6)

    folium.Marker(
        location=coord1, # coordinates for the marker
        popup=city1, # pop-up label for the marker
        icon=folium.Icon(color='green', icon_color='white', icon='ok-sign', angle=0, prefix='glyphicon')).add_to(m)
    folium.Marker(
        location=coord2, # coordinates for the marker
        popup=city2, # pop-up label for the marker
        icon=folium.Icon(color='lightgreen', icon_color='white', icon='ok-sign', angle=0, prefix='glyphicon')).add_to(m)
    folium.Marker(
        location=coord3, # coordinates for the marker
        popup=city3, # pop-up label for the marker
        icon=folium.Icon(color='lightgreen', icon_color='white', icon='ok-sign', angle=0, prefix='glyphicon')).add_to(m)
    return m
