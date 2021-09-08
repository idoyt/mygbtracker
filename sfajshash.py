imgs = [(1,),(2,),(3,),(4,),(5,),(6,)]
img = []

for i in range(1, len(imgs)+1):
    img.append((f"url_for('static', filename='images/{i}.jpg')",) + (i,))
    print((imgs[i-1]))
print(img)
