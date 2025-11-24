import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./AuthContext";
import { Spinner, Container  } from "react-bootstrap";

export const ProtectedRoute = () => {
    const { user, loading } = useAuth();

   
    if (loading) return (
        <Container
            fluid
            className="d-flex justify-content-center align-items-center"
            style={{ height: "100vh" }}
        >
            <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
            </Spinner>
        </Container>
    );

    return user ? <Outlet /> : <Navigate to="/login" replace />;
};

export const AdminRoute = () => {
    const { user, loading } = useAuth();

    if (loading) return null;

    const allowed = user?.role === "admin" || user?.role === "educator";

    return user && allowed ? <Outlet /> : <Navigate to="/login" replace />;
};
