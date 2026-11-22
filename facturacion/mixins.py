class UsuarioRegistroMixin:
    def form_valid(self, form):
        if self.request.user.is_authenticated and not form.instance.user_id:
            form.instance.user = self.request.user
        return super().form_valid(form)