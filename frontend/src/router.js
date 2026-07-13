import { createRouter, createWebHistory } from "vue-router";

import Login from "./Login.vue";
import Register from "./Register.vue";
import AdminDashboard from "./AdminDashboard.vue";
import StaffDashboard from "./StaffDashboard.vue";
import UserDashboard from "./UserDashboard.vue";
import Treks from "./Treks.vue";
import TrekDetails from "./TrekDetails.vue";

const routes = [
    {
        path: "/",
        redirect: "/login"
    },

    {
        path: "/login",
        component: Login
    },

    {
        path: "/register",
        component: Register
    },

    {
        path: "/treks",
        component: Treks,
        meta: { requiresAuth: true }
    },

    {
        path: "/treks/:id",
        component: TrekDetails,
        props: true,
        meta: { requiresAuth: true }
    },

    {
        path: "/admin",
        component: AdminDashboard,
        meta: {
            requiresAuth: true,
            role: "Admin"
        }
    },

    {
        path: "/staff",
        component: StaffDashboard,
        meta: {
            requiresAuth: true,
            role: "Trek Staff"
        }
    },

    {
        path: "/dashboard",
        component: UserDashboard,
        meta: {
            requiresAuth: true,
            role: "User"
        }
    },

    {
        path: "/:pathMatch(.*)*",
        redirect: "/login"
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {

    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    // Protected route
    if (to.meta.requiresAuth && !token) {
        return next("/login");
    }

    // Role protected
    if (to.meta.role && role !== to.meta.role) {

        if (role === "Admin")
            return next("/admin");

        if (role === "Trek Staff")
            return next("/staff");

        if (role === "User")
            return next("/dashboard");

        return next("/login");
    }

    // Already logged in
    if (
        token &&
        (to.path === "/login" || to.path === "/register")
    ) {

        if (role === "Admin")
            return next("/admin");

        if (role === "Trek Staff")
            return next("/staff");

        if (role === "User")
            return next("/dashboard");
    }

    next();
});

export default router;