new Vue({
      el: '#detail',
      data: {
        detail:{}
      },
      methods: {
        
      },
      mounted() {
        if (localStorage.getItem('detail')) {
            try {
              this.detail = JSON.parse(localStorage.getItem('detail'));
              
            } catch(e) {
              localStorage.removeItem('detail');
            }
          }
        },

    });


new Vue({
  el: '#searchbar',
  data: function() {
        return {
          restaurants: [],
          state1: '',
          query: ''
        }
      },
  
  methods: {
    search(){
          var _self = this;
          axios
            .post(ip_address+'/engine/search?query='+JSON.stringify(this.query),{
  })
            .then(function (response) {
              console.log(response);
               localStorage.setItem('results',JSON.stringify(response.data.ret));
               sessionStorage.setItem('cur_query',response.data.query);
               setTimeout(() => { window.location.href = 'result.html'; }, 2000);
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
  mounted() {
    if (sessionStorage.getItem('cur_query')) {
      try{
        this.query=sessionStorage.getItem('cur_query').replace(/^\"|\"$/g,'');
      }catch(e) {
              sessionStorage.removeItem('cur_query');
            }
  }
}

});