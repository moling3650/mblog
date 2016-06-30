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
        comment: '',
        comments: [],
        message:''
    },
    filters: {
        marked: marked
    },
    methods: {
        submit: function() {
            var self = this;
            if (! self.comment.trim()) {
                return showAlert(self, '请输入评论内容！');
            }
            postJSON('/api/blogs/' + self.id + '/comments', {
                content: self.comment,
                time: (self.comments[0] && self.comments[0].created_at) || 0
            }, function (err, data) {
                if (err) {
                    return showAlert(self, err.message || err.data || err);
                }
                self.comment = '';
                self.comments = data.comments.concat(self.comments);
            })
        }
    },
    ready: function() {
        var self = this;
        getJSON('/api/blogs/' + self.id + '/comments', function (err, data) {
            if (err) {
                return alert(err.message || err.data || err);
                }
            self.comments = data.comments;
        });
    }
});
