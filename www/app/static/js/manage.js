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
            'comments': {'user_name': '作者', 'content':'内容'}
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
            $.getJSON('/api/' + this.table, {
                page: page || '1',
                size: size || '10'
            }, function (data) {
                vm.items = data.items;
                vm.page = data.page;
            })
        },
        delete_item: function (item) {
            if (confirm('确认要删除“' + (item.name || item.content) + '”？删除后不可恢复！')) {
                postJSON('/api/' + this.table + '/' + item.id + '/delete', function (err, r) {
                    vm.items.$remove(item);
                    if (vm.items.length === 0 && vm.page.index > 1) {
                        vm.getItemsByPage(vm.page.index - 1, vm.page.limit);
                    }
                    else if (vm.items.length < 10 && vm.page.index < vm.page.last) {
                        vm.getItemsByPage(vm.page.index, vm.page.limit);
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
