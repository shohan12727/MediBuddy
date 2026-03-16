import { createBrowserRouter } from "react-router";
import ErrorPage from "../Components/ErrorPage";
import Root from "../Root/Root";
import Home from "../Pages/Home";


export const router = createBrowserRouter([
  {
    path: "/",
    errorElement: <ErrorPage />,
    Component: Root,
    children: [
      {
        index: true,
        Component: Home,
      },
    ],
  },
]);