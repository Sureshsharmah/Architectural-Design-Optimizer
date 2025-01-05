from flask import Flask, render_template, request, send_from_directory
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os
import random

app = Flask(__name__)

# Folder to store images
app.config['UPLOAD_FOLDER'] = 'static/images/'

# Function to simulate energy efficiency optimization
def optimize_energy_efficiency():
    energy_consumption = [500, 350]  # Hypothetical values (pre and post optimization)
    return energy_consumption

# Function to simulate material usage reduction
def optimize_material_usage():
    materials = ['Concrete', 'Steel', 'Glass', 'Wood']
    pre_optimization = [500, 300, 150, 200]
    post_optimization = [400, 250, 120, 180]
    return materials, pre_optimization, post_optimization

# Function to simulate carbon footprint reduction
def optimize_carbon_footprint():
    carbon_footprint = {'Concrete': 0.5, 'Steel': 0.8, 'Glass': 0.3, 'Wood': 0.4}
    return carbon_footprint

# Function to generate random report data
def generate_report():
    data = []
    for i in range(10):  # 10 rows
        row = [random.randint(100, 1000) for _ in range(10)]  # 10 columns with random values
        data.append(row)
    return data

# Function to generate 3D bar chart
def generate_3d_bar_chart():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create random data for the chart
    x = np.arange(5)
    y = np.arange(5)
    x, y = np.meshgrid(x, y)
    z = np.zeros_like(x)

    dx = np.ones_like(z) * 0.8
    dy = np.ones_like(z) * 0.8
    dz = np.random.randint(1, 100, size=z.shape)

    ax.bar3d(x.flatten(), y.flatten(), z.flatten(), dx.flatten(), dy.flatten(), dz.flatten(), color='c', alpha=0.8)

    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('3D Optimization Visualization')

    chart_path = os.path.join(app.config['UPLOAD_FOLDER'], '3d_chart.png')
    plt.savefig(chart_path)
    plt.close()
    return chart_path

# Route to render the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to generate and display optimization results
@app.route('/optimize', methods=['POST'])
def optimize():
    energy_data = optimize_energy_efficiency()
    materials, pre_materials, post_materials = optimize_material_usage()
    carbon_footprint = optimize_carbon_footprint()

    # Generate energy efficiency plot
    plt.figure(figsize=(8, 5))
    plt.bar(['Pre-Optimization', 'Post-Optimization'], energy_data, color=['red', 'green'])
    plt.title('Energy Efficiency Comparison')
    plt.ylabel('Energy Consumption (kWh/day)')
    plt.xlabel('Design')
    energy_plot_path = os.path.join(app.config['UPLOAD_FOLDER'], 'energy_efficiency.png')
    plt.savefig(energy_plot_path)
    plt.close()

    # Generate material usage reduction plot
    plt.figure(figsize=(8, 5))
    bar_width = 0.35
    index = np.arange(len(materials))
    plt.bar(index, pre_materials, bar_width, label='Pre-Optimization', color='red')
    plt.bar(index + bar_width, post_materials, bar_width, label='Post-Optimization', color='green')
    plt.title('Material Usage Reduction')
    plt.xlabel('Material')
    plt.ylabel('Material Usage (kg)')
    plt.xticks(index + bar_width / 2, materials)
    plt.legend()
    material_plot_path = os.path.join(app.config['UPLOAD_FOLDER'], 'material_reduction.png')
    plt.savefig(material_plot_path)
    plt.close()

    # Generate carbon footprint reduction plot
    pre_footprint = sum([pre_materials[i] * carbon_footprint[materials[i]] for i in range(len(materials))])
    post_footprint = sum([post_materials[i] * carbon_footprint[materials[i]] for i in range(len(materials))])

    plt.figure(figsize=(8, 5))
    plt.bar(['Pre-Optimization', 'Post-Optimization'], [pre_footprint, post_footprint], color=['red', 'green'])
    plt.title('Carbon Footprint Reduction')
    plt.ylabel('Carbon Footprint (kg CO2)')
    plt.xlabel('Design')
    footprint_plot_path = os.path.join(app.config['UPLOAD_FOLDER'], 'carbon_footprint.png')
    plt.savefig(footprint_plot_path)
    plt.close()

    # Generate 3D bar chart
    chart_path = generate_3d_bar_chart()

    # Generate report data
    report_data = generate_report()

    return render_template('results.html', energy_plot='images/energy_efficiency.png',
                           material_plot='images/material_reduction.png', footprint_plot='images/carbon_footprint.png',
                           report_data=report_data, chart_path='images/3d_chart.png')

# Route to render the results page
@app.route('/results')
def results():
    return render_template('results.html')

# Route to serve images from the static folder
@app.route('/static/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
