/**
 *
 * @authors moling (365024424@qq.com)
 * @date    2016-06-23 14:07:56
 * @version $Id$
 */

function validateEmail(email) {
  var re = /^[\w\.\-]+\@[\w\-]+(\.[\w\-]+){1,4}$/;
  return re.test(email);
}

var vmRegister = new Vue({
    el: '#vm-form',
    data: {
        name: '',
        email: '',
        password: '',
        password2: '',
        message:''
    },
    methods: {
        submit: function(){
            this.name = this.name.trim();
            this.email = this.email.trim();
            if (! this.name) {
                return showAlert(this, '请输入名字');
            }
            if (! validateEmail(this.email)) {
                return showAlert(this, '请输入正确的Email地址');
            }
            if (this.password.length < 6) {
                return showAlert(this, '口令长度至少为6个字符');
            }
            if (this.password !== this.password2) {
                return showAlert(this, '两次输入的口令不一致');
            }
            var data = {
                name: this.name,
                email: this.email,
                sha1_pw: CryptoJS.SHA1(this.email + ':' + this.password).toString()
            }
            postJSON('/register', data, function (err, result) {
                if (err) {
                    return showAlert(vmRegister, err.message || err.data || err);
                }
                return location.assign('/');
            });
        }
    }
});