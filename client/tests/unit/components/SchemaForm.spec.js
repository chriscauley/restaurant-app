import { shallowMount } from '@vue/test-utils'

import SchemaForm, { prepSchema } from '@/components/SchemaForm'
import api from '@/common/api'

jest.mock('@/common/api')

test('prepSchema sets custom fields', () => {
  const hidden_field = { __widget: 'HiddenInput' }

  const schema = {
    type: 'object',
    properties: {
      avatar_url: {},
      photo_url: {},
      hidden_field,
    },
  }
  const preppedSchema = prepSchema(schema)
  expect(preppedSchema.properties.hidden_field.ui.tagName).toBe('ur-hidden')
  expect(preppedSchema.properties.avatar_url.type).toBe('image')
  expect(preppedSchema.properties.photo_url.title).toBe('Photo')
  expect(schema.properties.avatar_url).toStrictEqual({})
})

test('SchemaForm loads schema via api', async next => {
  const schema = { properties: {} }
  const propsData = {
    form_name: 'dummy_schema',
  }
  api._mock.get(propsData.form_name + '/?schema=1', { schema })

  const wrapper = shallowMount(SchemaForm, { propsData })
  expect(wrapper.vm.schema).toBe(undefined)
  await Promise.resolve()
  expect(wrapper.vm.schema).toStrictEqual(schema)
  api._mock.cleanUp()
  next()
})

test('SchemaForm.submit', async next => {
  const schema = { properties: {} }
  const form_name = 'submit_schema'
  const propsData = { form_name }
  api._mock.get(form_name + '/?schema=1', { schema })

  const wrapper = shallowMount(SchemaForm, { propsData })
  await Promise.resolve()

  // submit causes schema to refetch
  api._mock.get(form_name + '/?schema=1', { schema })
  api._mock.post(form_name + '/', { throw: 'arst' })
  wrapper.vm.submit({})
  expect(wrapper.vm.loading).toBe(true)

  // submitting twice does not trigger submit again (unsure how to test this)
  wrapper.vm.submit({})

  await Promise.resolve()
  await Promise.resolve()
  expect(wrapper.vm.loading).toBe(false)
  api._mock.post(form_name + '/', {})
  wrapper.vm.submit({})
  await Promise.resolve()
  await Promise.resolve()
  next()
})
