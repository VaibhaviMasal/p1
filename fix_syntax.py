
path = 'c:/Users/Vaibhavi/OneDrive/Documents/Student_Feedback_System/templates/dashboard.html'
with open(path, 'r') as f:
    content = f.read()

# Replace the bad syntax
new_content = content.replace('{ {', '{{').replace('} }', '}}')

with open(path, 'w') as f:
    f.write(new_content)

print("Fixed syntax in dashboard.html")
