import ui from '@/store/ui'

test('ui.toasts are shown and hidden', done => {
  ui.state.DELAY = 0
  expect(ui.state.toasts.length).toBe(0)
  ui.toast({})
  expect(ui.state.toasts.length).toBe(1)
  setTimeout(() => {
    expect(ui.state.toasts[0].hidden).toBe(true)
    ui.state.toasts.pop()
    done()
  }, 10)
})

test('ui.alert', () => {
  expect(ui.state.alert).toBe(null)
  ui.alert('foo')
  expect(ui.state.alert).toBe('foo')
  ui.closeAlert()
  expect(ui.state.alert).toBe(null)
})
