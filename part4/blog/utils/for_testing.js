const { test, describe, beforeEach } = require('node:test')
const assert = require('node:assert')
const listHelper = require('./list_helper');
const User =  require('../users')
const bcrypt = require('bcrypt')
test('dummy returns one', () => {
  const blogs = []

  const result = listHelper.dummy(blogs)
  assert.strictEqual(result, 1)
})
describe('total likes', () => {
  const listWithOneBlog = [
    {
      _id: '5a422aa71b54a676234d17f8',
      title: 'Go To Statement Considered Harmful',
      author: 'Edsger W. Dijkstra',
      url: 'https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf',
      likes: 5,
      __v: 0
    }
  ]
  const withemptylist = [ ]
  const listWithManyBlog = [
    {
      _id: '5a422aa71b54a676234d17f8',
      title: 'Go To Statement Considered Harmful',
      author: 'Edsger W. Dijkstra',
      url: 'https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf',
      likes: 5,
      __v: 0
    },
    {
      _id: '5nssa71b54a676234d17f8',
      title: 'Go To Statement Cisonsidered Harmful',
      author: 'Edsger W. Da0ijkstra',
      url: 'https://hosaepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf',
      likes: 5,
      __v: 0
    },
    {
      _id: '5nssa67h54a676234d17f8',
      title: 'Test 3',
      author: 'Edsger W. Da0ia',
      url: 'test.pdf',
      likes: 5,
      __v: 0
    }
  ]

  test('when list has only one blog, equals the likes of that', () => {
    const result = listHelper.totalLikes(listWithOneBlog)
    assert.strictEqual(result, 5)
  })
  test('of emptylist is zero', () => {
    const result = listHelper.totalLikes(withemptylist)
    assert.strictEqual(result, 0)
  })
  test('listWithManyBlog', () => {
    const result = listHelper.totalLikes(listWithManyBlog)
    assert.strictEqual(result, 15)
  })
})



describe('favoriteBlog', () => {
  const listWithOneBlog = [
    {
      _id: '5a422aa71b54a676234d17f8',
      title: 'Go To Statement Considered Harmful',
      author: 'Edsger W. Dijkstra',
      url: 'https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf',
      likes: 5,
      __v: 0
    }
  ]
  const withemptylist = [ ]
  const listWithManyBlog = [
    {
      _id: '5a422aa71b54a676234d17f8',
      title: 'Go To Statement Considered Harmful',
      author: 'Edsger W. Dijkstra',
      url: 'https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf',
      likes: 5,
      __v: 0
    },
    {
      _id: '5nssa71b54a676234d17f8',
      title: 'Go To Statement Cisonsidered Harmful',
      author: 'Edsger W. Da0ijkstra',
      url: 'https://hosaepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf',
      likes: 5,
      __v: 0
    },
    {
      _id: '5nssa67h54a676234d17f8',
      title: 'Test 3',
      author: 'Edsger W. Da0ia',
      url: 'test.pdf',
      likes: 5,
      __v: 0
    }
  ]
  const listWithnotequal = [
    {
      _id: '5a422aa71b54a676234d17f8',
      title: 'Go To Statement Considered Harmful',
      author: 'Edsger W. Dijkstra',
      url: 'https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf',
      likes: 5,
      __v: 0
    },
    {
      _id: '5nssa71b54a676234d17f8',
      title: 'Go To Statement Cisonsidered Harmful',
      author: 'Edsger W. Da0ijkstra',
      url: 'https://hosaepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf',
      likes: 5,
      __v: 0
    },
    {
      _id: '5nssa67h54a676234d17f8',
      title: 'Test 3',
      author: 'Edsger W. Da0ia',
      url: 'test.pdf',
      likes: 15,
      __v: 0
    }
  ]
  test('when list has only one blog, equals the likes of that', () => {
    const result = listHelper.favoriteBlog(listWithOneBlog)
    console.log(result)
    const expected = {
      _id: '5a422aa71b54a676234d17f8',
      title: 'Go To Statement Considered Harmful',
      author: 'Edsger W. Dijkstra',
      url: 'https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf',
      likes: 5,
      __v: 0
    }
    assert.deepStrictEqual(result, expected)
  })
  test('of emptylist is zero', () => {
    const result = listHelper.favoriteBlog(withemptylist)
    assert.strictEqual(result, null)
  })
  test('listWithManyBlog', () => {
    const result = listHelper.favoriteBlog(listWithManyBlog)
    
    const expected = {
      _id: '5nssa67h54a676234d17f8',
      title: 'Test 3',
      author: 'Edsger W. Da0ia',
      url: 'test.pdf',
      likes: 5,
      __v: 0
    }
    assert.deepStrictEqual(result, expected)
  })

  test('list With not equal', () => {
    const result = listHelper.favoriteBlog(listWithnotequal)
    
    const expected = {
      _id: '5nssa67h54a676234d17f8',
      title: 'Test 3',
      author: 'Edsger W. Da0ia',
      url: 'test.pdf',
      likes: 15,
      __v: 0
    }
    assert.deepStrictEqual(result, expected)
  })

})
describe('mostBlog', () => {
  test('return most blogs', () => {
    const blogs = [
      {
        _id: '5a422aa71b54a676234d17f8',
        title: 'Go To Statement Considered Harmful',
        author: 'Edsger W. Dijkstra',
        url: 'https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf',
        likes: 5,
        __v: 0
      },
      {
        _id: '5nssa71b54a676234d17f8',
        title: 'Go To Statement Cisonsidered Harmful',
        author: 'Edsger W. Dijkstra',
        url: 'https://hosaepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf',
        likes: 5,
        __v: 0
      },
      {
        _id: '5nssa67h54a676234d17f8',
        title: 'Test 3',
        author: 'Edsger W. Da0ia',
        url: 'test.pdf',
        likes: 15,
        __v: 0
      }
    ]

    const result = listHelper.mostBlogs(blogs)
    console.log(result)
    const expected = { author: 'Edsger W. Dijkstra', blogs: 2 }
    assert.deepStrictEqual(result, expected)
  })


  test('of emptylist is zero', () => {
      const withemptylist = [ ]
      const result = listHelper.mostBlogs(withemptylist)
      console.log(result)
      console.log("hi")
      
      assert.strictEqual(result, null)
    })

})
describe('mostLikes', () => {
  test('return most blogs', () => {
    const blogs = [
      {
        _id: '5a422aa71b54a676234d17f8',
        title: 'Go To Statement Considered Harmful',
        author: 'Edsger W. Dijkstra',
        url: 'https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf',
        likes: 25,
        __v: 0
      },
      {
        _id: '5nssa71b54a676234d17f8',
        title: 'Go To Statement Cisonsidered Harmful',
        author: 'Edsger W. Dijkstra',
        url: 'https://hosaepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf',
        likes: 5,
        __v: 0
      },
      {
        _id: '5nssa67h54a676234d17f8',
        title: 'Test 3',
        author: 'Edsger W. Da0ia',
        url: 'test.pdf',
        likes: 15,
        __v: 0
      }
    ]

    const result = listHelper.mostLikes(blogs)
    console.log(result)
    const expected = { author: 'Edsger W. Dijkstra', likes: 30 }
    assert.deepStrictEqual(result, expected)
  })


  test('of emptylist is zero', () => {
      const withemptylist = [ ]
      const result = listHelper.mostLikes(withemptylist)
      console.log(result)
      console.log("hi")
      
      assert.strictEqual(result, null)
    })

})
