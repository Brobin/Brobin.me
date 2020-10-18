import request from "request-promise-native";
import {
  BlogPostListParams,
  BlogPostListResponse,
  BlogSidebarResponse,
} from "../types/Blog";

const baseUrl =
  process.env.NODE_ENV === "production"
    ? `${window.location.origin}/api`
    : "http://127.0.0.1:8000/api";

interface ApiInterface {
  listPosts: (params: BlogPostListParams) => Promise<BlogPostListResponse>;
  getBlogSidebar: () => Promise<BlogSidebarResponse>;
}

class Api implements ApiInterface {
  async listPosts(params: BlogPostListParams): Promise<BlogPostListResponse> {
    return this.get(`/blog?page=${params.page}`);
  }

  async getBlogSidebar(): Promise<BlogSidebarResponse> {
    return this.get("/blog/sidebar");
  }

  async post(route: string, params = {}) {
    const requestOptions = {
      url: `${baseUrl}${route}`,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params),
    };
    const response = await request(requestOptions);
    return JSON.parse(response);
  }

  async get(route: string, parseJson = true) {
    const requestOptions = {
      url: `${baseUrl}${route}`,
      method: "GET",
      headers: { "Content-Type": "application/json" },
    };
    const response = await request(requestOptions);
    if (parseJson) {
      return JSON.parse(response);
    }
    return response;
  }
}

const api = new Api();

export default api;
