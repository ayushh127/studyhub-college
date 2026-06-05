import json
import os

LOG_FILE = r"C:\Users\Ayush\.gemini\antigravity\brain\6733cf40-5222-4464-8e46-183e4bb9a366\.system_generated\logs\transcript.jsonl"
TARGET_FILES = [
    r"d:\StudyHub\app\routes\student.py",
    r"d:\StudyHub\app\templates\student\dashboard.html",
    r"d:\StudyHub\app\templates\student\quizzes.html",
    r"d:\StudyHub\app\templates\student\quiz_attempt_exam.html",
    r"d:\StudyHub\app\templates\student\quiz_attempt_learning.html",
    r"d:\StudyHub\app\templates\student\quiz_result.html",
    r"d:\StudyHub\app\templates\student\quiz_review.html",
    r"d:\StudyHub\app\templates\student\quiz_start.html",
    r"d:\StudyHub\app\templates\student\select_college.html"
]

def recover_files():
    file_contents = {f: "" for f in TARGET_FILES}
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
            except:
                continue
                
            if 'tool_calls' in data:
                for call in data['tool_calls']:
                    if call.get('name') == 'write_to_file':
                        args = call.get('args', {})
                        target = args.get('TargetFile', '')
                        if isinstance(target, str) and target.startswith('"'):
                            target = json.loads(target)
                        
                        code = args.get('CodeContent', '')
                        if isinstance(code, str) and code.startswith('"'):
                            try:
                                code = json.loads(code)
                            except:
                                pass
                                
                        for tf in TARGET_FILES:
                            if tf.lower().replace('\\', '/') == str(target).lower().replace('\\', '/'):
                                file_contents[tf] = code
                                
                    elif call.get('name') == 'replace_file_content':
                        args = call.get('args', {})
                        target = args.get('TargetFile', '')
                        if isinstance(target, str) and target.startswith('"'):
                            target = json.loads(target)
                        for tf in TARGET_FILES:
                            if tf.lower().replace('\\', '/') == str(target).lower().replace('\\', '/'):
                                # if we have a replacement, just apply it to our tracked file_contents
                                target_content = args.get('TargetContent', '')
                                if isinstance(target_content, str) and target_content.startswith('"'):
                                    target_content = json.loads(target_content)
                                replacement_content = args.get('ReplacementContent', '')
                                if isinstance(replacement_content, str) and replacement_content.startswith('"'):
                                    replacement_content = json.loads(replacement_content)
                                    
                                if target_content in file_contents[tf]:
                                    file_contents[tf] = file_contents[tf].replace(target_content, replacement_content)
                                    
                    elif call.get('name') == 'multi_replace_file_content':
                        args = call.get('args', {})
                        target = args.get('TargetFile', '')
                        if isinstance(target, str) and target.startswith('"'):
                            target = json.loads(target)
                        
                        chunks = args.get('ReplacementChunks', '[]')
                        if isinstance(chunks, str):
                            try:
                                chunks = json.loads(chunks)
                            except:
                                chunks = []
                                
                        for tf in TARGET_FILES:
                            if tf.lower().replace('\\', '/') == str(target).lower().replace('\\', '/'):
                                for chunk in chunks:
                                    target_content = chunk.get('TargetContent', '')
                                    replacement_content = chunk.get('ReplacementContent', '')
                                    if target_content in file_contents[tf]:
                                        file_contents[tf] = file_contents[tf].replace(target_content, replacement_content)
    
    for tf, content in file_contents.items():
        if content:
            with open(tf, 'w', encoding='utf-8') as out:
                out.write(content)
            print(f"Recovered {tf}")
        else:
            print(f"Could not find full content for {tf} in write_to_file calls.")

if __name__ == '__main__':
    recover_files()
