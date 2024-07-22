import { type NextRequest, NextResponse } from "next/server";
import { getCookie, setCookie } from "cookies-next";
import { Api } from "./ApiService";

export async function middleware(req: NextRequest) {
  const url = req.nextUrl;
  const res = NextResponse.next();
  const access = getCookie("access", { res, req });
  const refresh = getCookie("refresh", { res, req });

  if (access === undefined && refresh !== undefined) {
    try {
      const response = await fetch(Api.Refresh, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          refresh: refresh,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        if (data.access) {
          setCookie("access", data.access, { res, req, maxAge: data.expire });
        } else {
          if (url.pathname !== "/newUser") {
            return NextResponse.redirect(new URL("/newUser", req.url));
          }
        }
      }
    } catch {
      return NextResponse.redirect(new URL("/newUser", req.url));
    }
  } else if (access && refresh && url.pathname !== "/proUser") {
    // return NextResponse.redirect(new URL("/proUser", req.url));
  } else if (
    url.pathname === "/" &&
    access === undefined &&
    refresh === undefined
  ) {
    return NextResponse.redirect(new URL("/newUser", req.url));
  } else if (url.pathname === "/proUser" && refresh === undefined) {
    return NextResponse.redirect(new URL("/newUser", req.url));
  } else if (url.pathname === "newUser" && refresh) {
    // return NextResponse.redirect(new URL("/proUser", req.url));
  } else if (url.pathname === "/" && refresh === undefined) {
    return NextResponse.redirect(new URL("/newUser", req.url));
  }

  return res;
}
