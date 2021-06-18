
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Login.vue')},
      { path: '/index', component: () => import('pages/Index.vue')},
      { path: '/reg', component: () => import('pages/register.vue')},
      { path: '/class', component: () => import('pages/Class.vue')},
      { path: '/manage', component: () => import('pages/Manage.vue')},
      { path: '/equip', component: () => import('pages/Equipment.vue')},
      { path: '/about', component: () => import('pages/About.vue')}
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
