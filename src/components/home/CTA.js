import { Link } from "react-router-dom";

export default function CTA() {
  return (
    <div className="bg-gray-50">
      <div className="mx-auto max-w-full py-12  lg:flex lg:items-center lg:justify-between lg:py-16 ">
        <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          <span className="block">Ready to dive in?</span>
          <span className="block text-orange-button">
            Start your free trial today.
          </span>
        </h2>
        <div className="mt-8 flex lg:mt-0 lg:flex-shrink-0">
          <div className="inline-flex rounded-md shadow">
            <Link
              to="/"
              className="inline-flex items-center justify-center rounded-md border border-transparent bg-orange-button px-5 py-3 text-base font-medium text-white hover:bg-gray-900"
            >
              Get started
            </Link>
          </div>
          <div className="ml-3 inline-flex rounded-md shadow">
            <Link
              to="/"
              className="inline-flex items-center justify-center rounded-md border border-transparent bg-white px-5 py-3 text-base font-medium text-orange-button hover:bg-indigo-50"
            >
              Learn more
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
