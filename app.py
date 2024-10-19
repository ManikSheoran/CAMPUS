from flask import Flask, render_template, request
import heapq
from waitress import serve

app = Flask(__name__)

# Dijkstra's algorithm
def dijkstra(graph, s):
    queue = []
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}
    distances[s] = 0
    heapq.heappush(queue, (0, s))

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances[current_node]:
            continue

        for weight, node in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[node]:
                distances[node] = distance
                predecessors[node] = current_node
                heapq.heappush(queue, (distance, node))

    return distances, predecessors

# Helper to extract the shortest path
def get_shortest_path(predecessors, start, end):
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = predecessors[current]
    return path

campus = {
    '1st Gate': [(93, 'Rabindra Statue'), (138, 'Guest House')],
    'Rabindra Statue': [(93, '1st Gate'), (66, 'Guest House'), (80, 'Amenities')],
    'Guest House': [(138, '1st Gate'), (66, 'Rabindra Statue'), (66, 'I Hall'), (92, 'Graveyard')],
    'Amenities': [(80, 'Rabindra Statue'), (76, 'Richardson Hall'), (67, 'Netaji Bhavan')],
    'Netaji Bhavan': [(67, 'Amenities')],
    'I Hall': [(66, 'Guest House'), (130, 'Main Building'), (44, 'I Canteen')],
    'Main Building': [(130, 'I Hall'), (100, 'Library')],
    'Library': [(100, 'Main Building'), (97, 'H14'), (103, 'D Quarters')],
    'I Canteen': [(44, 'I Hall'), (122, 'SNT')],
    'SNT': [(122, 'I Canteen'), (66, 'Cafe Inn'), (90, 'BE Model School'), (210, 'MN Dastur')],
    'Cafe Inn': [(66, 'SNT')],
    'H14': [(97, 'Library')],
    'Sen Hall': [(44, 'H15'), (56, 'Macdonald Hall')],
    'H15': [(44, 'Sen Hall'), (30, 'Sengupta Hall')],
    'H13': [(55, 'Neem Lake'), (266, 'LT Williams Hall')],
    'Sengupta Hall': [(30, 'H15'), (24, 'H16')],
    'H16': [(24, 'Sengupta Hall')],
    'Macdonald Hall': [(56, 'Sen Hall'), (85, 'Richardson Hall')],
    'Richardson Hall': [(85, 'Macdonald Hall'), (76, 'Amenities')],
    'Pandya Hall': [(82, 'Clock Tower')],
    'Graveyard': [(92, 'Guest House'), (46, 'Clock Tower'), (165, 'MN Dastur')],
    'Clock Tower': [(46, 'Graveyard'), (195, 'Madhusudan Bhavan'), (82, 'Pandya Hall'), (65, 'Hospital'), (60, 'Wolfenden Hall'), (143, 'BE Model School')],
    'Hospital': [(65, 'Clock Tower')],
    'Wolfenden Hall': [(60, 'Clock Tower'), (42, 'Nivedita Hall')],
    'Nivedita Hall': [(42, 'Wolfenden Hall'), (76, 'Oval'), (66, 'H10')],
    'Oval': [(76, 'Nivedita Hall'), (135, 'Madhusudan Bhavan')],
    'Madhusudan Bhavan': [(135, 'Oval'), (195, 'Clock Tower')],
    'BE Model School': [(143, 'Clock Tower'), (90, 'SNT'), (196, 'LT Williams Hall')],
    'Gymnasium': [(178, 'LT Williams Hall')],
    'H10': [(266, 'LT Williams Hall'), (66, 'Nivedita Hall'), (130, 'H11'), (60, 'H9')],
    'H11': [(130, 'H10'), (49, 'Neem Lake'), (40, 'H7')],
    'H7': [(40, 'H11'), (70, 'H8')],
    'H8': [(70, 'H7'), (50, 'H9')],
    'H9': [(50, 'H8'), (60, 'H10'), (92, '2nd Gate')],
    'Neem Lake': [(55, 'H13'), (49, 'H11'), (180, 'LT Williams Hall')],
    'LT Williams Hall': [(196, 'BE Model School'), (180, 'Neem Lake'), (178, 'Gymnasium'), (266, 'H10'), (260, '3rd Gate')],
    '3rd Gate': [(260, 'LT Williams Hall')],
    '2nd Gate': [(92, 'H9')],
    'D Quarters': [(103, 'Library')],
    'MN Dastur': [(165, 'Graveyard'), (210, 'SNT')],
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        source = request.form.get('source')
        destination = request.form.get('destination')

        # Run Dijkstra's algorithm
        distances, predecessors = dijkstra(campus, source)
        path = get_shortest_path(predecessors, source, destination)
        
        # Render the result back to the user
        return render_template('index.html', path=' -> '.join(path), source=source, destination=destination)
    
    return render_template('index.html')

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)

