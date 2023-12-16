let wallpaper = [
  'bg_default.jpg',
  'bg_eiffel.jpg',
  'bg_girl.jpg',
  'bg_vae.jpg',
  'bg_1.jpg',
  'bg_2.jpg',
  'bg_3.jpg',
  'bg_4.jpg',
  'bg_5.jpg',
  'bg_6.jpg',
  'bg_7.jpg',
  'bg_8.jpg',
  'bg_9.jpg',
  'bg_10.jpg',
  'bg_11.jpg',
  'bg_12.jpg',
  'bg_13.jpg',
  'bg_14.jpg',
  'bg_15.jpg'
]

wallpaper = wallpaper.map(item => {
  return '/static/images/' + item
})

export default wallpaper
