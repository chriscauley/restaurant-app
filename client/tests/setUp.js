import { JSDOM } from 'jsdom'
import { config } from '@vue/test-utils'
import store from '@/store'
import SchemaForm from '@/components/SchemaForm'
import Modal from '@/components/Modal'

jest.mock('@/common/api') // eslint-disable-line

const dom = new JSDOM()
global.document = dom.window.document
global.window = dom.window

config.global.mocks['$store'] = store
const Dummy = () => ''
const RouterLink = Dummy
const UrForm = Dummy
config.global.components = { SchemaForm, Modal, RouterLink, UrForm }
