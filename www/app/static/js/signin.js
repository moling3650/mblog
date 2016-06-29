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
            this.email = this.email.trim();
            if(! this.email ){
                return showAlert(vm, '请输入email');
            }
            var data = {
                email: this.email,
                sha1_pw: this.password==='' ? '' : CryptoJS.SHA1(this.email + ':' + this.password).toString()
            }
            postJSON('/authenticate', data, function(err, result){
                if (err) {
                    console.log(err);
                    return showAlert(vm, err.message || err.data || err);
                }
                location.assign('/');
            });
        }
    }
});
