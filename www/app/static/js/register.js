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
        name: getUrlParams('name') || '',
        email: '',
        password: '',
        password2: '',
        message:''
    },
    methods: {
        submit: function(){
            var self = this;
            self.name = self.name.trim();
            self.email = self.email.trim();
            if (! self.name) {
                return showAlert(self, '请输入名字');
            }
            if (! validateEmail(self.email)) {
                return showAlert(self, '请输入正确的Email地址');
            }
            if (self.password.length < 6) {
                return showAlert(self, '口令长度至少为6个字符');
            }
            if (self.password !== self.password2) {
                return showAlert(self, '两次输入的口令不一致');
            }
            postJSON('/register', {
                name: self.name,
                email: self.email,
                sha1_pw: CryptoJS.SHA1(self.email + ':' + self.password).toString(),
                oid: getUrlParams('oid'),
                image: getUrlParams('image')
            }, function (err, result) {
                if (err) {
                    return showAlert(self, err.message || err.data || err);
                }
                return location.assign(location.pathname.split('register')[0]);
            });
        }
    }
});