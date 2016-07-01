/**
 *
 * @authors moling (365024424@qq.com)
 * @date    2016-06-29 02:25:49
 * @version $Id$
 */


var vm = new Vue({
    el: '#blog',
    data: {
        action: '/api/blogs',
        message: '',
        blog: {
            name: '',
            summary: '',
            content: ''
        }
    },
    ready: function () {
        if (location.pathname.split('/').pop() === 'edit') {
            var id = getUrlParams('id');
            this.action = this.action + '/' + id;
            getJSON('/api/blogs/' + id, function (err, blog) {
                vm.blog = blog;
            });
        }
    },
    methods: {
        submit: function () {
            postJSON(this.action, this.blog, function (err, blog) {
                if (err) {
                    return showAlert(vm, err.message || err.data || err)
                }
                return location.assign(location.pathname.split('manage')[0] + 'blog/' + blog.id);
            });
        }
    }
});

