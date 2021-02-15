new Vue({
      el: '#searchbar',
      data: function() {
        return {
            query: '',
          
          state1: '',
          state2: ''
        }
      },
      methods: {
        currRole(selVal){
          this.role = selVal;
          sessionStorage.setItem('role', this.role);
        },
        getCookie (name) {
          var value = '; ' + document.cookie
          var parts = value.split('; ' + name + '=')
          if (parts.length === 2) return parts.pop().split(';').shift()
        },
        search(){
          var _self = this;
          axios
            .post('http://127.0.0.1:8080/engine/search?query='+JSON.stringify(this.query),{
            },{headers: {'X-CSRFToken': this.getCookie('csrftoken')}})
            .then(function (response) {
              console.log(response);
              displayContent(response.data);
            })
          
        },
        querySearch(queryString, cb) {
              var restaurants = this.restaurants;
              var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
              // 调用 callback 返回建议列表的数据
              cb(results);
            },
            createFilter(queryString) {
              return (restaurant) => {
                  return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
              };
            },
            loadAll() {
            return [];
        },
            handleSelect(item) {
              console.log(item);
            }
        
      },
          // mounted() {
          //   // this.restaurants = this.loadAll();
          // }
    });
function displayContent(content){
  var p = document.getElementById("content");
  p.innerHTML=content;
}