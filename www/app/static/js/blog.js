/**
 *
 * @authors moling (365024424@qq.com)
 * @date    2016-06-25 17:54:28
 * @version $Id$
 */
var blog = new Vue({
    el: '#blog',
    data: {
        id: location.pathname.split('/').pop(),
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
            postJSON('/api/blogs/' + this.id + '/comments', {
                content: this.content,
                time: (this.comments[0] && this.comments[0].created_at) || 0
            }, function (err, data) {
                if (err) {
                    return alert(err.message || err.data || err);
                }
                blog.content = '';
                blog.comments = data.comments.concat(blog.comments);
            })
        }
    },
    ready: function() {
        var blog_id = location.pathname.split('/').pop();
        getJSON('/api/blogs/' + this.id + '/comments', function (err, data) {
            if (err) {
                return alert(err.message || err.data || err);
                }
            blog.comments = data.comments;
        });
    }
});
