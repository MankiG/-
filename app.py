import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)

# 设置上传文件夹
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 检查文件扩展名是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 主页路由，返回HTML页面
@app.route('/')
def index():
    return render_template('index.html')

# 处理音频文件上传并执行攻击
@app.route('/start_attack', methods=['POST'])
def start_attack():
    if 'vc_tgt' not in request.files or 'adv_tgt' not in request.files or 'source' not in request.files:
        return '没有选择所有必要的文件', 400
    
    # 获取上传的音频文件
    vc_tgt_file = request.files['vc_tgt']
    adv_tgt_file = request.files['adv_tgt']
    source_file = request.files['source']

    # 检查文件是否有效
    if vc_tgt_file and allowed_file(vc_tgt_file.filename):
        vc_tgt_filename = secure_filename(vc_tgt_file.filename)
        vc_tgt_file.save(os.path.join(app.config['UPLOAD_FOLDER'], vc_tgt_filename))
    if adv_tgt_file and allowed_file(adv_tgt_file.filename):
        adv_tgt_filename = secure_filename(adv_tgt_file.filename)
        adv_tgt_file.save(os.path.join(app.config['UPLOAD_FOLDER'], adv_tgt_filename))
    if source_file and allowed_file(source_file.filename):
        source_filename = secure_filename(source_file.filename)
        source_file.save(os.path.join(app.config['UPLOAD_FOLDER'], source_filename))
    
    # 默认将vc_tgt设置为vc_src
    vc_src_filename = vc_tgt_filename

    # 获取用户输入的扰动因子（epsilon）和迭代次数（iterations）
    epsilon = request.form.get('epsilon', '0.075')  # 默认值为0.075
    iterations = request.form.get('iterations', '1500')  # 默认值为1500

    # 生成命令行执行语句
    command = [
        'python', 'attack.py', 
        'model/',  # 模型目录路径
        os.path.join(app.config['UPLOAD_FOLDER'], vc_tgt_filename),  # vc_tgt
        os.path.join(app.config['UPLOAD_FOLDER'], adv_tgt_filename),  # adv_tgt
        os.path.join(app.config['UPLOAD_FOLDER'], 'output_defended.wav'),  # 输出文件路径
        '--vc_src', os.path.join(app.config['UPLOAD_FOLDER'], vc_src_filename),  # vc_src 默认与 vc_tgt 一致
        '--eps', epsilon,
        '--n_iters', iterations,
        '--attack_type', 'e2e'  # 默认攻击类型为e2e
    ]

    # 执行命令行
    try:
        subprocess.run(command, check=True)
        # 返回生成的对抗性音频文件
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], 'output_defended.wav'), mimetype='audio/wav')
    except subprocess.CalledProcessError as e:
        return f"命令执行失败: {e}", 500

# 运行Flask应用
if __name__ == '__main__':
    app.run(debug=True)
