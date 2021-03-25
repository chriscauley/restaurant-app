import { range } from 'lodash'

export default {
  data() {
    return { current_page: 1 }
  },
  computed: {
    has_next_page() {
      return this.pages[this.pages.length - 1]?.next_page
    },
    pages() {
      return range(1, this.current_page + 1).map(this.getPage)
    },
  },
  methods: {
    getPage() {
      throw 'Paginated component must specify a getPage function'
    },
    loadNextPage() {
      this.current_page++
    },
  },
}
