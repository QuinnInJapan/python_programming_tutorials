import json
import os

def generate_html_from_schema(schema):
    """Generate HTML content from a JSON schema."""
    html = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{} - {}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="unit-info">{}課題 {}</span>
            <span class="lesson-info">{}レッスン {}</span>
        </div>
        <h1>{}</h1>
    """.format(
        schema['unit_title'], schema['lesson_title'],
        schema['unit_number'], schema['unit_title'],
        schema['lesson_number'], schema['lesson_title'],
        schema['lesson_title']
    )
    
    for section in schema['sections']:
        if 'header' in section:  # Check if 'header' exists
            html += "<h2>{}</h2>".format(section['header'])
        
        if section['type'] == 'introduction':
            html += "<div class='section'><p>{}</p></div>".format(section.get('content', ''))
        
        elif section['type'] == 'concept':
            content = section.get('content', '').replace("\\n", "<br>")
            html += "<div class='section concept'><p>{}</p></div>".format(content)
        
        elif section['type'] == 'code-example':
            html += "<div class='code'>{}</div>".format(section.get('code', ''))
        
        elif section['type'] == 'tasks':
            html += "<div class='section task'>"
            for task in section.get('tasks', []):
                html += """
                <div class="task-item">
                    <h3>{}</h3>
                    <p>{}</p>
                    <div class='code'>{}</div>
                    <p><strong>出力例</strong></p>
                    <div class='code'>{}</div>
                </div>
                """.format(
                    task.get('title', ''),
                    task.get('description', ''),
                    task.get('code', ''),
                    task.get('expected_output', '')
                )
            html += "</div>"
        
        elif section['type'] == 'fix':
            html += "<div class='section fix'><p>{}</p><ul>".format(section.get('description', ''))
            for i, example in enumerate(section.get('examples', []), start=1):
                html += """
                <li>
                    <h4>問題 {}</h4>
                    <div class='code'>{}</div>
                    <p><strong>期待される出力</strong></p>
                    <div class='code'>{}</div>
                </li>
                """.format(
                    i,
                    example.get('broken_code', ''),
                    example.get('desired_output', '')
                )
            html += "</ul></div>"
        
        elif section['type'] == 'experiments':
            html += "<div class='section experiment'>"
            for experiment in section.get('experiments', []):
                html += """
                <div class="experiment">
                    <p>{}</p>
                    <div class='code'>{}</div>
                    <p><strong>出力例</strong></p>
                    <div class='code'>{}</div>
                </div>
                """.format(
                    experiment.get('description', ''),
                    experiment.get('code', ''),
                    experiment.get('expected_output', '')
                )
            html += "</div>"
    html += "</div></body></html>"
    return html

# Ensure the "lessons" subdirectory exists
output_directory = "lessons"
os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir('.'):
    if filename.startswith('lesson') and filename.endswith('.json'):
        lesson_number = filename[6:-5]
        with open(filename, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        html_output = generate_html_from_schema(schema)
        output_filename = os.path.join(output_directory, f"lesson{lesson_number}.html")
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_output)
        print(f"Generated {output_filename} from {filename}")
