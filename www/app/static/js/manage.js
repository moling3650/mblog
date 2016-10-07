/**
 *
 * @authors moling (365024424@qq.com)
 * @date    2016-06-26 21:07:03
 * @version $Id$
 */

var vm = new Vue({
    el: '#vm',
    data: {
        table: location.pathname.split('/').pop(),
        items: [],
        page: null,
        models: {
            'users': {'name': '名字', 'email': '电子邮箱'},
            'blogs': {'name': '标题', 'user_name': '作者'},
            'comments': {'user_name': '作者', 'content':'内容'},
        },
    },
    computed:{
        fields: function () {
            return this.models[this.table];
        }
    },
    ready: function () {
        this.getItemsByPage(getUrlParams('page'), getUrlParams('size'));
    },
    methods: {
        getItemsByPage: function  (page, size) {
            var self = this;
            $.ajax({
                url: '/api/v2.0/' + this.table,
                data: {
                    page: page || '1',
                    size: size || '10'
                },
                success: function(data) {
                    self.items = data.items;
                    self.page = data.page;
                }
            })
        },
        delete_item: function (item) {
            var self = this;
            if (confirm('确认要删除“' + (item.name || item.content) + '”？删除后不可恢复！')) {
                $.ajax({
                    url: '/api/v2.0/' + this.table.slice(0, -1) + '/' + item.id,
                    type: 'DELETE',
                    success: function() {
                        self.items.$remove(item);
                        if (self.items.length === 0 && self.page.index > 1) {
                            self.getItemsByPage(self.page.index - 1, self.page.limit);
                        }
                        else if (self.items.length < 10 && self.page.index < self.page.last) {
                            self.getItemsByPage(self.page.index, self.page.limit);
                        }
                    }
                });
            }
        },
        vaildPage: function(i) {
            return (i > 1) && (Math.abs(i - this.page.index) < 3);
        },
        gotoPage: function (page) {
            return this.getItemsByPage(page, this.page.limit);
        }
    }
});
