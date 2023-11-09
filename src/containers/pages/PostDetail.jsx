import { connect } from "react-redux";
import Layout from "hocs/layouts/Layout";
import Navbar from "components/navigation/Navbar";
import Footer from "components/navigation/Footer";
import { Link, useParams } from "react-router-dom";
import { useEffect } from "react";
import { get_blog } from "redux/actions/blog/blog";
import moment from "moment";
import DOMPurify from "dompurify";

function PostDetail({ get_blog, post }) {
  const params = useParams();
  const slug = params.slug;

  useEffect(() => {
    window.scrollTo(0, 0);
    get_blog(slug);
  }, []);

  return (
    <Layout>
      <Navbar />
      {post && post.slug === slug ? (
        <div className="pt-24">
          <div className="relative mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
            <div className="min-w-0 flex-1">
              <h1 className="pb-8 text-4xl font-bold tracking-tight text-black sm:text-5xl lg:text-6xl">
                {post.title}
              </h1>
              <span className=" hover:text-orange-500  mx-1 font-medium text-gray-800 text-sm ">
                <Link to={`/category/${post.category.slug}`}>
                  {post.category.name}
                </Link>
              </span>{" "}
              <span className="text-gray-300">&middot;</span>
              <span className="mt-2 ml-2 mr-1 font-medium text-gray-800 text-sm">
                {moment(post.published).format("LL")}
              </span>{" "}
              <span className="text-gray-300">&middot;</span>
              <span className="mt-2 mx-2 font-medium text-gray-800 text-sm">
                {post.time_read} min read
              </span>
              <p className="mt-4 text-lg font-regular text-gray-800 leading-8">
                {post.description}
              </p>
            </div>
          </div>

          <figure>
            <img
              className="w-11/12 max-w-5xl max-h-96 m-auto object-cover object-center"
              src={post.thumbnail}
              alt=""
            />
          </figure>

          <div className="relative overflow-hidden bg-white py-16">
            <div className="relative px-4 sm:px-6 lg:px-8">
              <div className="prose prose-lg max-w-6xl prose-indigo mx-auto mt-6 text-gray-500">
                <p
                  dangerouslySetInnerHTML={{
                    __html: DOMPurify.sanitize(post.content),
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      ) : (
        <>Loading</>
      )}
      <Footer />
    </Layout>
  );
}

const mapStateToProps = (state) => ({
  post: state.blog.post,
});

export default connect(mapStateToProps, {
  get_blog,
})(PostDetail);
