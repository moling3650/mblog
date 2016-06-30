/**
 *
 * @authors moling (365024424@qq.com)
 * @date    2016-06-23
 * @version $Id$
 */

var vm = new Vue({
    el: '#vm-form',
    data: {
        email: '',
        password: '',
        message: ''
    },
    methods: {
        submit: function(){
            var self = this;
            self.email = self.email.trim();
            if(! self.email ){
                return showAlert(self, '请输入email');
            }
            postJSON('/authenticate', {
                email: self.email,
                sha1_pw: self.password==='' ? '' : CryptoJS.SHA1(self.email + ':' + self.password).toString()
            }, function(err, result){
                if (err) {
                    return showAlert(self, err.message || err.data || err);
                }
                return location.assign(location.pathname.split('signin')[0]);
            });
        }
    }
});
