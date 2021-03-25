import PaginatedMixin from '@/mixins/PaginatedMixin'
import { shallowMount } from '@vue/test-utils'

const PaginatedComponent = {
  render: () => '',
  mixins: [PaginatedMixin],
  methods: {
    getPage(page) {
      return {
        value: page ** 2,
        next_page: page < 2,
      }
    }
  }
}

test('PaginatedMixin', () => {
  expect(PaginatedMixin.methods.getPage).toThrow('Paginated component must specify a getPage function')

  const wrapper = shallowMount(PaginatedComponent)

  expect(wrapper.vm.current_page).toBe(1)
  expect(wrapper.vm.pages.length).toBe(1)
  expect(wrapper.vm.has_next_page).toBe(true)

  wrapper.vm.loadNextPage()

  expect(wrapper.vm.current_page).toBe(2)
  expect(wrapper.vm.pages.length).toBe(2)
  expect(wrapper.vm.has_next_page).toBe(false)

})