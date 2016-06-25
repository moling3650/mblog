/**
 *
 * @authors moling (365024424@qq.com)
 * @date    2016-06-25 17:54:28
 * @version $Id$
 */

var blog_id = location.pathname.split('/').pop();

var vm = new Vue({
    el: '#vm',
    data: {
        content: '',
        comments: []
    },
    filters: {
        marked: marked
    },
    methods: {
        submit: function() {
            if (! this.content.trim()) {
                return alert('请输入评论内容！');
            }
            postJSON('/api/blogs/' + blog_id + '/comments', {
                content: this.content.trim(),
                time: (this.comments.length) ? vm.comments[0].created_at : 0
            }, function (err, data) {
                if (err) {
                    return alert(err.message || err.data || err);
                }
                vm.content = '';
                vm.comments = data.comments.concat(vm.comments);
            })
        }
    }
});

$(function() {
    getJSON('/api/blogs/' + blog_id + '/comments', function (err, data) {
        if (err) {
            return alert(err);
        }
        vm.comments = data.comments;
    });
});
