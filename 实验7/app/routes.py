from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import current_user, login_required, login_user
from wtforms.validators import ValidationError
from .models import User, db
from flask_wtf.csrf import validate_csrf

bp = Blueprint('routes', __name__)

SPECIAL_INVITE_CODE = "admin"


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        real_name = request.form['real_name']
        email = request.form['email']
        invite_code = request.form['invite_code']

        # 检查密码和确认密码是否匹配
        if password != confirm_password:
            return render_template('register.html', message='Passwords do not match.')

        # 检查用户名是否已经存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', message='Username already exists.')

        # 创建新用户并保存到数据库
        # 判断是管理员还是用户
        role = 'admin' if invite_code == SPECIAL_INVITE_CODE else 'user'
        new_user = User(username=username, role=role, real_name=real_name, email=email)
        new_user.set_password(password)  # 设置哈希密码

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('routes.login'))

    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash('Invalid username or password', 'error')
            return redirect(url_for('routes.login'))

        login_user(user, remember=remember)

        next_page = request.args.get('next')
        return redirect(next_page or url_for('routes.profile'))
    return render_template('login.html')


@bp.route('/profile')
@login_required
def profile():
    if current_user.is_admin:
        all_users = User.query.all()
        return render_template('profile.html', user=current_user, all_users=all_users)
    return render_template('profile.html', user=current_user)


@bp.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('routes.index'))


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        real_name = request.form.get('real_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')

        # 检查是否要修改密码
        if old_password:
            # 检查旧密码是否匹配
            if not current_user.check_password(old_password):
                flash('Old password is incorrect', 'error')
                return redirect(url_for('routes.edit_profile'))
        # 检查是否输入了新密码
        if new_password and confirm_password:
            # 检查两次输入新密码是否匹配
            if new_password != confirm_password:
                flash('New password and confirm password do not match', 'error')
                return redirect(url_for('routes.edit_profile'))

        # 更新用户信息
        if new_password:
            current_user.set_password(new_password)
        if real_name:
            current_user.real_name = real_name
        if age:
            current_user.age = age
        if gender:
            current_user.gender = gender
        if phone:
            current_user.phone = phone
        if email:
            current_user.email = email
        if address:
            current_user.address = address
        db.session.commit()

        flash('Profile updated successfully', 'success')
        return redirect(url_for('routes.profile'))

    return render_template('edit_profile.html', user=current_user)


@bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    # 验证 CSRF 令牌
    try:
        validate_csrf(request.form['csrf_token'])
    except ValidationError:
        return jsonify({'success': False, 'message': 'CSRF token invalid'}), 403

    user = User.query.get_or_404(user_id)
    if user.is_admin():
        return jsonify({'success': False, 'message': 'Cannot delete an administrator'}), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'User deleted successfully'})


@bp.route('/view_user/<int:user_id>')
@login_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('view_user_profile.html', user=user)


@bp.route('/edit_user_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        real_name = request.form.get('real_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')

        # 检查是否要修改密码
        if old_password:
            # 检查旧密码是否匹配
            if not current_user.check_password(old_password):
                flash('Old password is incorrect', 'error')
                return redirect(url_for('routes.edit_user_profile', user_id=user.id))
        # 检查是否输入了新密码
        if new_password and confirm_password:
            # 检查两次输入新密码是否匹配
            if new_password != confirm_password:
                flash('New password and confirm password do not match', 'error')
                return redirect(url_for('routes.edit_user_profile', user_id=user.id))

        # 更新用户信息
        if new_password:
            user.set_password(new_password)
        if real_name:
            user.real_name = real_name
        if age:
            user.age = age
        if gender:
            user.gender = gender
        if phone:
            user.phone = phone
        if email:
            user.email = email
        if address:
            user.address = address
        db.session.commit()

        flash('Profile updated successfully', 'success')
        return redirect(url_for('routes.view_user', user_id=user.id))

    return render_template('edit_user_profile.html', user=user)