const dummy = (blogs) => {
    return 1


  
}
const totalLikes= (blogs) => {
    const reducer = (sum, blog) => {
      console.log(sum + blog.likes)

    return sum + blog.likes;
    
  }
  console.log(blogs.reduce(reducer, 0))
  return blogs.reduce(reducer, 0)
}

const favoriteBlog = (blogs) => {
  if (blogs.length === 0) {
    console.log("empty");
    return null;
  }
 
  
  const reducer = (current, maxb) => {

    if (current.likes > maxb.likes) {
      return current; 
    } else {
      return maxb; 
    }
  }
  const fav = blogs.reduce(reducer);

    
  console.log(fav)
  return fav
    


  
}
  
const mostBlogs  = (blogs) => {
  console.log(blogs.length)
  if (blogs.length === 0) {
    console.log("empty");
    return null;
  }
  console.log("blog")
  
  const reducer = (tally_writers,current) => {

   if (current.author in tally_writers) { 
      tally_writers[current.author] ++ ; 
    } else {
      tally_writers[current.author]= 1; 
    }
    console.log(tally_writers)
    return tally_writers;
   };
  
  const fav = blogs.reduce(reducer, {});
  const famous = (current, maxb) => {
    console.log("check")
    console.log(current, maxb)

    if (fav[current] > fav[maxb] ) {
      return current; 
    } else {
      return maxb; 
    }
  }
  const authors = Object.keys(fav);
  console.log(authors)
  const most = authors.reduce(famous);
  console.log("final")
  console.log(most)

  
    return {author: most,blogs: fav[most]};

}
const mostLikes  = (blogs) => {
  console.log(blogs.length)
  if (blogs.length === 0) {
    console.log("empty");
    return null;
  }
  console.log("blog")
  
  const reducer = (tally_writers,current) => {

   if (current.author in tally_writers) { 
      tally_writers[current.author] = tally_writers[current.author]+current.likes ; 
    } else {
      tally_writers[current.author]= current.likes; 
    }
    console.log(tally_writers)
    return tally_writers;
   };
  
  const fav = blogs.reduce(reducer, {});
  console.log(fav)
  const famous = (current, maxb) => {
    console.log("check")
    console.log(current, maxb)

    if (fav[current] > fav[maxb] ) {
      return current; 
    } else {
      return maxb; 
    }
  }
  const authors = Object.keys(fav);
  console.log(authors)
  const most = authors.reduce(famous);
  console.log("final")
  console.log(most)
  return {author: most,likes: fav[most]};
  
}
  

module.exports = {
  dummy,
  totalLikes,
  favoriteBlog,
  mostBlogs,
  mostLikes


}