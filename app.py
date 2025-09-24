from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import cv2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# ---------- Home Page ----------
@app.route('/')
def index():
    return render_template('index.html')


# ---------- Upload Image ----------
@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file uploaded"

    file = request.files['image']
    if file.filename == '':
        return "No file selected"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    return render_template('edit.html', filename=file.filename)


# ---------- Apply Operation ----------
@app.route('/edit/<filename>', methods=['POST'])
def edit(filename):
    operation = request.form['operation']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = cv2.imread(filepath)

    if img is None:
        return "Error loading image"

    # --- Operations ---
    if operation == "grayscale":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    elif operation == "flip":
        img = cv2.flip(img, 1)

    elif operation == "rotate":
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    elif operation == "resize":
        img = cv2.resize(img, (200, 200))

    elif operation == "crop":
        img = img[50:250, 50:250]

    elif operation == "text":
        cv2.putText(img, "Hello!", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    elif operation == "line":
        cv2.line(img, (0, 0), (img.shape[1], img.shape[0]), (255, 0, 0), 5)

    elif operation == "rectangle":
        cv2.rectangle(img, (50, 50), (200, 200), (0, 255, 0), 3)

    elif operation == "circle":
        cv2.circle(img, (150, 150), 50, (0, 255, 255), -1)

    # Save result
    result_filename = "result.jpg"
    result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)

    if len(img.shape) == 2:  # Fix grayscale saving
        cv2.imwrite(result_path, cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))
    else:
        cv2.imwrite(result_path, img)

    return render_template('result.html', filename=result_filename)


# ---------- Serve Images ----------
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)
